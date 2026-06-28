"""
Script untuk cek data PMI dari website BP2MI
Version: v3 (Proven working di VPS)
"""

import asyncio
import re
import sys
import json
from playwright.async_api import async_playwright


async def cek_pmi_batch(passports):
    """Batch check PMI data from BP2MI"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        results = {}

        for paspor in passports:
            print(f"🔍 Checking: {paspor}")
            try:
                await page.goto(
                    'https://siskop2mi.bp2mi.go.id/publik/cek_status',
                    timeout=20000
                )
                await page.wait_for_load_state('networkidle')

                # Isi paspor
                await page.fill("input[name='t_paspor']", paspor)

                # Solve captcha (format: "4 + 4 = ?")
                captcha = await page.text_content('#captcha')
                match = re.search(r'(\d+)\s([+\-])\s+(\d+)', captcha or '')
                if match:
                    a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
                    ans = a + b if op == '+' else a - b if op == '-' else a * b
                    await page.fill("input[name='t_captcha']", str(ans))
                    print(f"   ✓ Captcha solved: {captcha.strip()} = {ans}")

                await page.locator("button#cek_status").click(force=True)
                await page.wait_for_timeout(3000)

                # Ambil data dari form-group
                data = await page.evaluate("""() => {
                    const r = {};
                    const h4 = document.querySelector('h4');
                    if (h4) r['No Registrasi'] = h4.textContent.trim();
                    document.querySelectorAll('.form-group').forEach(g => {
                        const l = g.querySelector('label');
                        const h5 = g.querySelector('h5');
                        if (l && h5) {
                            let t = l.textContent.trim();
                            const i = t.indexOf('/');
                            if (i > 0) t = t.substring(0, i).trim();
                            r[t] = h5.textContent.trim();
                        }
                    });
                    return r;
                }""")

                if data and len(data) > 0:
                    results[paspor] = data
                    print(f"   ✓ Data found: {len(data)} fields")
                else:
                    results[paspor] = {'Status': 'Tidak ditemukan'}
                    print(f"   ❌ Data tidak ditemukan")

            except Exception as e:
                error_msg = str(e)[:80]
                results[paspor] = {'Status': f'Error: {error_msg}'}
                print(f"   ❌ Error: {error_msg}")

        await browser.close()
        return results


async def cek_pmi(paspor):
    """Single check - return first result"""
    results = await cek_pmi_batch([paspor])
    return results.get(paspor)


async def main():
    """CLI interface"""
    passports = sys.argv[1:] if len(sys.argv) > 1 else ['AU610053']

    print("=" * 60)
    print("📋 CEK STATUS PMI — BP2MI (v3)")
    print("=" * 60)

    results = await cek_pmi_batch(passports)

    print("\n" + "=" * 60)
    print("📊 HASIL CEK PMI")
    print("=" * 60)

    for paspor, data in results.items():
        if data and 'Status' not in data:
            nama = data.get('Nama Lengkap', '-')
            negara = data.get('Negara Penempatan', '-')
            berlaku = data.get('Berlaku Hingga', '-')
            print(
                f"✅ {paspor}: {nama} | {negara} | {berlaku}"
            )
        else:
            status = data.get('Status', 'Unknown') if data else 'No response'
            print(f"❌ {paspor}: {status}")

    # Save JSON result
    with open('/tmp/hasil_pmi.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📁 JSON: /tmp/hasil_pmi.json")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
