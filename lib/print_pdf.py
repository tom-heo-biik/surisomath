# -*- coding: utf-8 -*-
"""수리소 학습지 PDF를 학원 프린터(EPSON EM-C800)로 뽑는다 — 100% 크기, 양면 긴 쪽 넘김, 품질 높게.

연마·시험대비·수행평가 PDF는 앞 절반이 학생 쪽, 뒤 절반이 선생님 쪽이다. 두 쪽의 부수를
따로 정한다. 한 부씩 따로 보내므로 쪽 수가 홀수여도 부마다 새 장에서 시작한다.

    python lib/print_pdf.py 삼각비.pdf --plan                       계획만(작업·장 수, 프린터 설정 확인)
    python lib/print_pdf.py 삼각비.pdf=4/2 원과직선.pdf=2/2 --go    학생 쪽 4부·선생님 쪽 2부, 원과직선은 2부·2부
    python lib/print_pdf.py 삼각비.pdf=1/0 --go                     학생 쪽만 한 부
    python lib/print_pdf.py 삼각비.pdf --pages 1-2 --go             1·2쪽만 한 부(--copies N)
    python lib/print_pdf.py 삼각비.pdf --pages 1-2 --dry-run out    Microsoft Print to PDF로 찍어 본다

PDF만 적으면 =1/1(학생 쪽 한 부, 선생님 쪽 한 부)이다. 적은 차례대로 나온다.
Windows 전용. pywin32·numpy·pymupdf가 필요하다. 품질 이름이 Epson 드라이버 고유라 다른 프린터면 멈춘다.

어떻게 뽑나
- 100%: 쪽을 프린터 해상도(600dpi)로 그려 1:1로 놓는다. 뷰어의 용지 맞춤을 거치지 않는다.
  인쇄 가능 영역이 종이 끝에서 PHYSICALOFFSET(3mm)만큼 들어와 있어 그만큼 당긴다.
  시험대비는 종이에서 가운데 세로선이 22.5cm면 100%다.
- 품질: 사용자 기본 PrintTicket에서 품질·해상도·양면·색만 바꿔 DEVMODE를 만든다. 사용자 기본값은
  건드리지 않는다. 표준 psk:High는 드라이버가 받지 않고 다른 값으로 바꾸므로 Epson 이름공간의
  HighQuality("높게")·FineStd("섬세하게")를 쓴다. 만든 DEVMODE를 되읽어 요청과 같을 때만 보낸다.
- 색: 래스터로 보내므로 색 없는 장은 흑백 설정으로 보낸다. 컬러 설정이면 검정 글자에 컬러 잉크가
  섞일 수 있다. 색 있는 장만 장(앞뒤 두 쪽) 단위로 끊어 컬러로 보낸다. 차례는 그대로다.
- 차례: 보내는 도중 프린터가 비면 스풀러가 뒤 작업을 앞 작업보다 먼저 내보내기도 한다(2026-09-23 겪었다).
  그래서 첫 작업만 빼고 StartDoc 직후, 쪽을 쓰기 전에 멈춰 둔다. 다 보낸 뒤 앞의 두 개만 풀고
  하나 끝날 때마다 다음 것을 푼다. 앞서 보낸 수리소 작업이 대기열에 있으면 다 빠진 뒤에 보낸다 —
  새 묶음의 첫 작업은 안 멈추므로 멈춰 있는 앞 묶음보다 먼저 나간다.
"""
from __future__ import annotations

import argparse
import base64
import ctypes
import ctypes.wintypes as wt
import json
import locale
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import fitz
import numpy as np
import win32print

PRINTER = "EPSON EM-C800 (Wi-Fi)"
TAG = "수리소 "              # 작업 이름이 이것으로 시작하면 수리소 인쇄로 본다(대기열 기다리기)
A4 = (595.28, 841.89)        # pt, 세로

# ── DEVMODE ─────────────────────────────────────────────────────────────
# PrintTicket은 .NET(System.Printing)으로만 다룰 수 있어 PowerShell에 맡긴다.
# -EncodedCommand로 넘기므로 파일 인코딩·실행 정책을 타지 않는다. 결과는 $OutDir에 쓴다.
DEVMODE_PS = r"""
$ErrorActionPreference = 'Stop'
$result = [ordered]@{ ok = $false }
try {
    Add-Type -AssemblyName System.Printing
    Add-Type -AssemblyName ReachFramework
    $PSF = 'http://schemas.microsoft.com/windows/2003/08/printing/printschemaframework'
    # 티켓마다 접두어가 다를 수 있어(ns0000 …) 이름공간으로 찾는다
    $URI = @{
        psk   = 'http://schemas.microsoft.com/windows/2003/08/printing/printschemakeywords'
        epson = 'http://schema.epson.net/printschema/business/v100'
    }
    $SHORT = @{}; foreach ($k in $URI.Keys) { $SHORT[$URI[$k]] = $k }

    function Short($node, $qname) {
        $i = $qname.IndexOf(':')
        if ($i -lt 0) { return $qname }
        $p = $SHORT[$node.GetNamespaceOfPrefix($qname.Substring(0, $i))]
        if (-not $p) { $p = $qname.Substring(0, $i) }
        return $p + ':' + $qname.Substring($i + 1)
    }
    function Real($doc, $short) {
        $i = $short.IndexOf(':')
        $p = $doc.DocumentElement.GetPrefixOfNamespace($URI[$short.Substring(0, $i)])
        if (-not $p) { throw "티켓에 $($short.Substring(0, $i)) 이름공간이 없다 — Epson 드라이버가 아니다" }
        return $p + ':' + $short.Substring($i + 1)
    }
    function Read-Ticket($ticket) {
        $x = New-Object System.Xml.XmlDocument
        $x.LoadXml((New-Object System.IO.StreamReader($ticket.GetXmlStream())).ReadToEnd())
        $ns = New-Object System.Xml.XmlNamespaceManager($x.NameTable)
        $ns.AddNamespace('psf', $PSF)
        $map = [ordered]@{}
        foreach ($f in $x.SelectNodes('/psf:PrintTicket/psf:Feature', $ns)) {
            $o = $f.SelectSingleNode('psf:Option', $ns)
            if ($o) { $map[(Short $f $f.name)] = Short $o $o.name }
        }
        foreach ($p in $x.SelectNodes('/psf:PrintTicket/psf:ParameterInit', $ns)) {
            $map[(Short $p $p.name)] = $p.InnerText.Trim()
        }
        return $map
    }

    $q = (New-Object System.Printing.LocalPrintServer).GetPrintQueue($Printer)
    $base = $q.UserPrintTicket
    $conv = New-Object System.Printing.Interop.PrintTicketConverter($Printer, $q.ClientPrintSchemaVersion)
    $want = [ordered]@{
        'psk:PageOutputQuality'                 = 'epson:HighQuality'
        'psk:PageResolution'                    = 'epson:FineStd'
        'psk:JobDuplexAllDocumentsContiguously' = 'psk:TwoSidedLongEdge'
        'psk:PageMediaSize'                     = 'psk:ISOA4'
        'psk:PageOrientation'                   = 'psk:Portrait'
    }
    foreach ($c in @(@('color', 'psk:Color'), @('mono', 'psk:Monochrome'))) {
        $x = New-Object System.Xml.XmlDocument
        $x.LoadXml((New-Object System.IO.StreamReader($base.GetXmlStream())).ReadToEnd())
        $ns = New-Object System.Xml.XmlNamespaceManager($x.NameTable)
        $ns.AddNamespace('psf', $PSF)
        $opts = [ordered]@{}
        foreach ($k in $want.Keys) { $opts[$k] = $want[$k] }
        $opts['psk:PageOutputColor'] = $c[1]
        foreach ($k in $opts.Keys) {
            $o = $x.SelectSingleNode("/psf:PrintTicket/psf:Feature[@name='$(Real $x $k)']/psf:Option", $ns)
            if (-not $o) { throw "티켓에 $k 항목이 없다" }
            $o.SetAttribute('name', (Real $x $opts[$k]))
        }
        $ms = New-Object System.IO.MemoryStream
        $x.Save($ms); $ms.Position = 0
        $req = New-Object System.Printing.PrintTicket($ms)
        $req.CopyCount = 1
        $valid = $q.MergeAndValidatePrintTicket($base, $req).ValidatedPrintTicket
        $dm = $conv.ConvertPrintTicketToDevMode($valid, [System.Printing.Interop.BaseDevModeType]::UserDefault)
        [IO.File]::WriteAllBytes((Join-Path $OutDir "devmode_$($c[0]).bin"), $dm)

        # 드라이버가 받는 것은 DEVMODE다 — 티켓이 아니라 DEVMODE를 되읽어 잰다
        $back = Read-Ticket ($conv.ConvertDevModeToPrintTicket($dm))
        $opts['psk:JobCopiesAllDocuments'] = '1'
        $diff = @(foreach ($k in $opts.Keys) { if ($back[$k] -ne $opts[$k]) { "$k = $($back[$k]) (요청 $($opts[$k]))" } })
        $got = [ordered]@{}
        foreach ($k in $opts.Keys) { $got[$k] = $back[$k] }
        $result[$c[0]] = [ordered]@{ settings = $got; diff = $diff }
    }
    $conv.Dispose()
    $result['ok'] = $true
} catch {
    $result['error'] = "$($_.Exception.Message)"
}
[IO.File]::WriteAllText((Join-Path $OutDir 'result.json'), ($result | ConvertTo-Json -Depth 5),
                        (New-Object System.Text.UTF8Encoding($false)))
"""


def _ps_str(s):
    return "'" + s.replace("'", "''") + "'"


def make_devmodes(printer):
    """컬러·흑백 DEVMODE 둘을 만들고 되읽어 요청과 같은지 잰다. 다르면 멈춘다."""
    tmp = Path(tempfile.mkdtemp(prefix="suriso_print_"))
    try:
        script = f"$Printer = {_ps_str(printer)}\n$OutDir = {_ps_str(str(tmp))}\n" + DEVMODE_PS
        enc = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", enc],
                           capture_output=True, timeout=180)
        out = tmp / "result.json"
        if not out.exists():
            err = r.stderr.decode(locale.getpreferredencoding(False), "replace").strip()
            sys.exit(f"DEVMODE를 못 만들었다 (PowerShell 종료 코드 {r.returncode})\n{err[-800:]}")
        res = json.loads(out.read_text("utf-8-sig"))
        if not res["ok"]:
            sys.exit(f"DEVMODE를 못 만들었다 — {res.get('error')}")
        bad = [f"  {c}: {d}" for c in ("color", "mono") for d in _as_list(res[c]["diff"])]
        if bad:
            sys.exit("드라이버가 요청한 설정을 바꿨다 — 멈춘다\n" + "\n".join(bad))
        return {c: (tmp / f"devmode_{c}.bin").read_bytes() for c in ("color", "mono")}, res
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _as_list(v):
    # ConvertTo-Json은 한 개짜리 배열을 값 하나로, 빈 배열을 null로 쓰기도 한다
    return [] if v is None else v if isinstance(v, list) else [v]


# ── GDI ─────────────────────────────────────────────────────────────────
BAND = 128                   # 이 높이(px)로 끊어 잉크 있는 상자만 보낸다
SRCCOPY = 0x00CC0020
LOGPIXELSX, LOGPIXELSY = 88, 90
PHYSICALWIDTH, PHYSICALHEIGHT = 110, 111
PHYSICALOFFSETX, PHYSICALOFFSETY = 112, 113

gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)


class DOCINFOW(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_int), ("lpszDocName", wt.LPCWSTR), ("lpszOutput", wt.LPCWSTR),
                ("lpszDatatype", wt.LPCWSTR), ("fwType", wt.DWORD)]


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wt.DWORD), ("biWidth", wt.LONG), ("biHeight", wt.LONG), ("biPlanes", wt.WORD),
                ("biBitCount", wt.WORD), ("biCompression", wt.DWORD), ("biSizeImage", wt.DWORD),
                ("biXPelsPerMeter", wt.LONG), ("biYPelsPerMeter", wt.LONG), ("biClrUsed", wt.DWORD),
                ("biClrImportant", wt.DWORD)]


class BITMAPINFO8(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wt.DWORD * 256)]


gdi32.CreateDCW.restype = wt.HDC
gdi32.CreateDCW.argtypes = [wt.LPCWSTR, wt.LPCWSTR, wt.LPCWSTR, ctypes.c_void_p]
gdi32.GetDeviceCaps.argtypes = [wt.HDC, ctypes.c_int]
gdi32.StartDocW.argtypes = [wt.HDC, ctypes.POINTER(DOCINFOW)]
for _fn in ("StartPage", "EndPage", "EndDoc", "AbortDoc", "DeleteDC"):
    getattr(gdi32, _fn).argtypes = [wt.HDC]
gdi32.StretchDIBits.restype = ctypes.c_int
gdi32.StretchDIBits.argtypes = [wt.HDC] + [ctypes.c_int] * 8 + [ctypes.c_void_p, ctypes.c_void_p, wt.UINT, wt.DWORD]

GRAY_PALETTE = (wt.DWORD * 256)(*[(i << 16) | (i << 8) | i for i in range(256)])


def open_dc(printer, devmode):
    buf = ctypes.create_string_buffer(devmode, len(devmode)) if devmode else None
    hdc = gdi32.CreateDCW("WINSPOOL", printer, None, buf)
    if not hdc:
        raise OSError(f"CreateDC 실패 (error {ctypes.get_last_error()})")
    caps = {k: gdi32.GetDeviceCaps(hdc, v) for k, v in dict(
        dpix=LOGPIXELSX, dpiy=LOGPIXELSY, physw=PHYSICALWIDTH, physh=PHYSICALHEIGHT,
        offx=PHYSICALOFFSETX, offy=PHYSICALOFFSETY).items()}
    return hdc, buf, caps


def draw_page(hdc, page, color, dpix, dpiy, offx, offy):
    pm = page.get_pixmap(matrix=fitz.Matrix(dpix / 72, dpiy / 72),
                         colorspace=fitz.csRGB if color else fitz.csGRAY, alpha=False)
    n = pm.n
    a = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.stride)[:, :pm.width * n]
    a = a.reshape(pm.height, pm.width, n)
    ink_all = (a < 255).any(axis=2)
    sent = 0
    for y0 in range(0, pm.height, BAND):
        ink = ink_all[y0:y0 + BAND]
        cols = np.flatnonzero(ink.any(axis=0))
        if not cols.size:
            continue
        rows = np.flatnonzero(ink.any(axis=1))
        ya, yb = y0 + rows[0], y0 + rows[-1] + 1
        xa, xb = cols[0], cols[-1] + 1
        w, h = int(xb - xa), int(yb - ya)
        sub = a[ya:yb, xa:xb]
        if color:
            sub = sub[:, :, ::-1]                       # DIB는 BGR
        rb = w * n
        buf = np.zeros((h, rb + (-rb) % 4), np.uint8)   # 줄 끝을 4바이트에 맞춘다
        buf[:, :rb] = sub.reshape(h, rb)
        bits = np.ascontiguousarray(buf[::-1]).tobytes()  # 아래에서 위로(bottom-up)
        if color:
            bmi = BITMAPINFOHEADER(40, w, h, 1, 24, 0, 0, 0, 0, 0, 0)
        else:
            bmi = BITMAPINFO8(BITMAPINFOHEADER(40, w, h, 1, 8, 0, 0, 0, 0, 256, 0), GRAY_PALETTE)
        r = gdi32.StretchDIBits(hdc, int(xa) - offx, int(ya) - offy, w, h, 0, 0, w, h,
                                bits, ctypes.byref(bmi), 0, SRCCOPY)
        if r in (0, -1):
            raise OSError(f"StretchDIBits 실패 (error {ctypes.get_last_error()})")
        sent += len(bits)
    return sent


def print_job(printer, devmode, job, output=None, hprinter=None, pause=False):
    hdc, keep, caps = open_dc(printer, devmode)
    try:
        di = DOCINFOW(ctypes.sizeof(DOCINFOW), job["name"], output, None, 0)
        jid = gdi32.StartDocW(hdc, ctypes.byref(di))
        if jid <= 0:
            raise OSError(f"StartDoc 실패 (error {ctypes.get_last_error()})")
        if pause:
            # 쪽을 쓰기 전에 멈춰 둔다 — 스풀 중에 프린터가 비어도 새치기하지 못하게
            try:
                win32print.SetJob(hprinter, jid, 0, None, win32print.JOB_CONTROL_PAUSE)
            except Exception:
                gdi32.AbortDoc(hdc)
                raise
        doc = fitz.open(job["path"])
        total = 0
        try:
            for pno in job["pages"]:
                if gdi32.StartPage(hdc) <= 0:
                    raise OSError("StartPage 실패")
                total += draw_page(hdc, doc[pno], job["color"], caps["dpix"], caps["dpiy"], caps["offx"], caps["offy"])
                if gdi32.EndPage(hdc) <= 0:
                    raise OSError("EndPage 실패")
            if gdi32.EndDoc(hdc) <= 0:
                raise OSError("EndDoc 실패")
        except Exception:
            gdi32.AbortDoc(hdc)
            raise
        finally:
            doc.close()
        return jid, total, caps
    finally:
        gdi32.DeleteDC(hdc)


# ── 대기열 ──────────────────────────────────────────────────────────────
JOB_STATUS_PAUSED = 0x1
STATUS_BITS = [(0x1, "Paused"), (0x2, "Error"), (0x4, "Deleting"), (0x8, "Spooling"), (0x10, "Printing"),
               (0x20, "Offline"), (0x40, "PaperOut"), (0x80, "Printed"), (0x200, "Blocked"),
               (0x400, "UserIntervention"), (0x1000, "Complete"), (0x2000, "Retained")]


def status_text(s):
    return ",".join(name for bit, name in STATUS_BITS if s & bit) or "Normal"


def keep_order(hp, ids):
    """보낸 차례대로 — 앞의 두 작업만 풀고 나머지는 멈춰 둔 채, 하나 끝날 때마다 다음 것을 푼다."""
    last = None
    while True:
        live = {j["JobId"]: j for j in win32print.EnumJobs(hp, 0, 999, 1)}
        pending = [i for i in ids if i in live]
        if not pending:
            print(time.strftime("%H:%M:%S"), "대기열 비었다", flush=True)
            return
        for i in pending[:2]:
            if live[i]["Status"] & JOB_STATUS_PAUSED:
                win32print.SetJob(hp, i, 0, None, win32print.JOB_CONTROL_RESUME)
        line = f"남은 {len(pending)} | " + " ".join(f"{i}[{status_text(live[i]['Status'])}]" for i in pending[:2])
        if line != last:
            print(time.strftime("%H:%M:%S"), line, flush=True)
            last = line
        time.sleep(4)


def wait_queue(hp, timeout=1800):
    """앞서 보낸 수리소 작업이 대기열에서 다 빠질 때까지 기다린다 — 그 사이에 끼어들지 않게."""
    t0, shown = time.time(), False
    while True:
        ours = [j for j in win32print.EnumJobs(hp, 0, 999, 1) if (j["pDocument"] or "").startswith(TAG)]
        if not ours:
            if shown:
                print(time.strftime("%H:%M:%S"), "앞 작업 끝", flush=True)
            return
        if not shown:
            print(time.strftime("%H:%M:%S"), f"앞 작업 {len(ours)}개가 끝나길 기다린다", flush=True)
            shown = True
        if time.time() - t0 > timeout:
            sys.exit("앞 작업이 30분 넘게 안 빠진다 — 멈춘 채 남은 작업이 있는지 대기열을 본다")
        time.sleep(5)


# ── 계획 ────────────────────────────────────────────────────────────────
def has_color(page):
    pm = page.get_pixmap(dpi=40, colorspace=fitz.csRGB, alpha=False)
    a = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.stride)[:, :pm.width * 3]
    a = a.reshape(pm.height, pm.width, 3).astype(np.int16)
    return bool(((a.max(axis=2) - a.min(axis=2)) > 24).any())


def segments(doc, pages):
    """쪽 목록을 장(앞뒤 두 쪽) 단위로 끊어 같은 색 설정끼리 묶는다."""
    out = []
    for k in range(0, len(pages), 2):
        sheet = pages[k:k + 2]
        color = any(has_color(doc[i]) for i in sheet)
        if out and out[-1][1] == color:
            out[-1][0].extend(sheet)
        else:
            out.append([sheet, color])
    return out


def page_text(pages):
    ns = [p + 1 for p in pages]
    if len(ns) > 1 and ns == list(range(ns[0], ns[-1] + 1)):
        return f"{ns[0]}~{ns[-1]}쪽"
    return "·".join(map(str, ns)) + "쪽"


def parse_spec(s):
    """'삼각비.pdf=4/2' → (경로, 학생 쪽 부수, 선생님 쪽 부수). 부수를 안 적으면 1/1."""
    m = re.fullmatch(r"(.+?)=(\d+)/(\d+)", s)
    return (Path(m[1]), int(m[2]), int(m[3]), True) if m else (Path(s), 1, 1, False)


def parse_pages(s, count):
    """'1-2,5' → [0, 1, 4]"""
    out = []
    for part in s.split(","):
        a, _, b = part.strip().partition("-")
        try:
            lo, hi = int(a), int(b or a)
        except ValueError:
            sys.exit(f"--pages {s}: 1-2 또는 1,3-4처럼 적는다")
        if not 1 <= lo <= hi <= count:
            sys.exit(f"--pages {s}: 1~{count}쪽 안이어야 한다")
        out.extend(range(lo - 1, hi))
    return out


def plan(specs, pages=None, copies=1):
    jobs = []
    for path, n_student, n_teacher, _ in specs:
        if not path.exists():
            sys.exit(f"없는 파일: {path}")
        doc = fitz.open(path)
        for p in doc:
            if abs(p.rect.width - A4[0]) > 1 or abs(p.rect.height - A4[1]) > 1:
                sys.exit(f"{path.name} {p.number + 1}쪽이 A4 세로가 아니다({p.rect.width:.0f}×{p.rect.height:.0f}pt) — 100%로 놓을 수 없다")
        label = re.sub(r"^수리소_", "", path.stem).replace("_", " ")
        if pages is not None:
            parts = [("", parse_pages(pages, doc.page_count), copies)]
        else:
            if doc.page_count % 2:
                sys.exit(f"{path.name}: {doc.page_count}쪽이라 학생 쪽과 선생님 쪽을 반으로 가를 수 없다 — --pages로 쪽을 정한다")
            half = doc.page_count // 2
            parts = [("학생 쪽", list(range(half)), n_student),
                     ("선생님 쪽", list(range(half, 2 * half)), n_teacher)]
        for part, pp, n in parts:
            segs = segments(doc, pp)
            for c in range(1, n + 1):
                for sheet_pages, color in segs:
                    head = " ".join(x for x in (TAG.strip(), label, part, f"{c}/{n}") if x)
                    name = f"{head} ({page_text(sheet_pages)}{', 컬러' if color else ''})"
                    jobs.append(dict(path=str(path), pages=sheet_pages, color=color, name=name))
        doc.close()
    return jobs


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(errors="replace")   # cp949 콘솔에서 못 찍는 글자로 죽지 않게
    ap = argparse.ArgumentParser(description="수리소 학습지 PDF를 100%·양면(긴 쪽)·품질 높게 뽑는다")
    ap.add_argument("pdf", nargs="+", help="PDF 또는 PDF=학생쪽부수/선생님쪽부수 (적지 않으면 1/1)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--plan", action="store_true", help="계획과 프린터 설정만 본다")
    g.add_argument("--dry-run", metavar="DIR", help="흑백·컬러 첫 작업을 Microsoft Print to PDF로 DIR에 찍어 본다")
    g.add_argument("--go", action="store_true", help="프린터로 보낸다")
    ap.add_argument("--pages", metavar="RANGE", help="이 쪽만(예: 1-2 또는 1,3-4). PDF 하나일 때만")
    ap.add_argument("--copies", type=int, default=1, help="--pages의 부수(기본 1)")
    ap.add_argument("--printer", default=PRINTER, help=f"프린터 이름(기본 {PRINTER})")
    args = ap.parse_args()

    specs = [parse_spec(s) for s in args.pdf]
    if args.pages is not None and (len(specs) > 1 or specs[0][3]):
        sys.exit("--pages는 부수(=N/M) 없이 PDF 하나에만 쓴다 — 부수는 --copies로")

    fitz.TOOLS.set_aa_level(0)   # 프린터가 벡터를 찍을 때처럼 가장자리를 계조 없이
    jobs = plan(specs, args.pages, args.copies)
    if not jobs:
        sys.exit("보낼 것이 없다 — 부수가 모두 0이다")
    sheets = sum((len(j["pages"]) + 1) // 2 for j in jobs)
    faces = sum(len(j["pages"]) for j in jobs)

    if args.dry_run:
        out_dir = Path(args.dry_run)
        out_dir.mkdir(parents=True, exist_ok=True)
        picks = [j for j in jobs if not j["color"]][:1] + [j for j in jobs if j["color"]][:1]
        for k, j in enumerate(picks, 1):
            out = out_dir / f"dry_{k}.pdf"
            out.unlink(missing_ok=True)
            _, total, caps = print_job("Microsoft Print to PDF", None, j, output=str(out))
            print(f"{j['name']} -> {out}  비트맵 {total / 1e6:.1f}MB  caps {caps}")
        return

    for i, j in enumerate(jobs, 1):
        print(f"{i:2d}. {j['name']}")
    print(f"작업 {len(jobs)}개, {faces}면, {sheets}장")

    dm, res = make_devmodes(args.printer)
    s = res["mono"]["settings"]
    print("프린터 설정(되읽음, 컬러·흑백 둘 다 요청대로): "
          f"품질 {s['psk:PageOutputQuality']} · 해상도 {s['psk:PageResolution']} · "
          f"양면 {s['psk:JobDuplexAllDocumentsContiguously']} · {s['psk:PageMediaSize']} {s['psk:PageOrientation']}")
    for c in ("mono", "color"):
        hdc, keep, caps = open_dc(args.printer, dm[c])
        gdi32.DeleteDC(hdc)
        if (caps["dpix"], caps["dpiy"]) != (600, 600):
            sys.exit(f"{c} 해상도가 600dpi가 아니다({caps['dpix']}×{caps['dpiy']}) — 멈춘다")
    print(f"프린터 해상도 {caps['dpix']}dpi, 인쇄 영역 시작 {caps['offx']}×{caps['offy']}px")

    hp = win32print.OpenPrinter(args.printer)
    ids = []
    try:
        queue = win32print.EnumJobs(hp, 0, 999, 1)
        print(f"대기열 {len(queue)}개" + "".join(
            f"\n  {q['JobId']} {q['pDocument']} [{status_text(q['Status'])}]" for q in queue))
        if args.plan:
            return
        wait_queue(hp)
        for i, j in enumerate(jobs, 1):
            jid, total, _ = print_job(args.printer, dm["color" if j["color"] else "mono"], j,
                                      hprinter=hp, pause=i > 1)
            ids.append(jid)
            print(f"{i:2d}/{len(jobs)} 보냄 (작업 {jid}{', 멈춤' if i > 1 else ''}) {j['name']}  비트맵 {total / 1e6:.1f}MB",
                  flush=True)
        print(f"다 보냄: 작업 {len(jobs)}개, {faces}면, {sheets}장 — 차례대로 푼다", flush=True)
        keep_order(hp, ids)
    finally:
        for jid in ids:   # 멈춘 채로 남기지 않는다
            try:
                win32print.SetJob(hp, jid, 0, None, win32print.JOB_CONTROL_RESUME)
            except Exception:
                pass
        win32print.ClosePrinter(hp)
    print("끝")


if __name__ == "__main__":
    main()
