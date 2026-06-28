"""
Script untuk cek data PMI dari website BP2MI
Menggunakan Playwright untuk web automation
"""

import asyncio
import re
import sys
import json
from playwright.async_api import async_playwright


async def cek_pmi_batch(passports):
    """Batch check PMI data from BP2MI"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()

        results = {}

        for paspor in passports:
            print(f"\n🔍 CEK: {paspor}")
            try:
                await page.goto(
                    'https://siskop2mi.bp2mi.go.id/publik/cek_status',
                    timeout=20000,
                    wait_until='domcontentloaded'
                )
                await page.wait_for_load_state('networkidle', timeout=10000)
                await page.wait_for_timeout(500)

                # Fill passport number
                await page.fill("input[name='t_paspor']", paspor)

                # Get & solve captcha (math: 5 + 3, 8 - 2)
                captcha_elem = await page.query_selector('#captcha')
                captcha_text = await captcha_elem.text_content() if captcha_elem else ''
                captcha_clean = captcha_text.replace('×', '*').replace('x', '*').replace('X', '*').replace('?', '').replace('=', '').strip()

                match = re.search(r'(\d+)\s*([+\-*])\s+(\d+)', captcha_clean)
                if match:
                    a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
                    answer = a + b if op == '+' else a - b if op == '-' else a * b
                    await page.fill("input[name='t_captcha']", str(answer))
                    print(f"   ✓ Captcha solved: {captcha_clean} = {answer}")
                else:
                    print(f"   ❌ Captcha tidak bisa dipecahkan")
                    results[paspor] = {'Status': 'Captcha error'}
                    continue

                # Click submit button
                try:
                    await page.locator("button#cek_status").click(force=True)
                except:
                    await page.click("button[type='submit']")

                # Wait for result page
                try:
                    await page.wait_for_url("**/publik/status_pmi/**", timeout=15000)
                except:
                    pass

                await page.wait_for_timeout(2000)

                # Extract data from page structure (label + h5 format)
                data = await page.evaluate("""() => {
                    const result = {};
                    const h4 = document.querySelector('h4');
                    if (h4) result['No Registrasi'] = h4.textContent.trim();

                    const groups = document.querySelectorAll('.form-group');
                    for (const group of groups) {
                        const label = group.querySelector('label');
                        const h5 = group.querySelector('h5');
                        if (label && h5) {
                            let labelText = label.textContent.trim();
                            const slashIdx = labelText.indexOf('/');
                            if (slashIdx > 0) {
                                labelText = labelText.substring(0, slashIdx).trim();
                            }
                            result[labelText] = h5.textContent.trim();
                        }
                    }
                    return result;
                }""")

                if data and len(data) > 0:
                    results[paspor] = data
                    print(f"   ✓ Data ditemukan: {len(data)} fields")
                else:
                    # Check for error modal
                    error_msg = await page.evaluate("""() => {
                        const modal = document.querySelector('.modal.show');
                        if (modal) return modal.textContent.trim();
                        return null;
                    }""")

                    if error_msg and 'Error' in error_msg:
                        msg = error_msg.replace('×', '').replace('OK', '').strip()
                        results[paspor] = {'Status': msg or 'Error'}
                        print(f"   ❌ Error: {msg}")
                    else:
                        results[paspor] = {'Status': 'Tidak ditemukan'}
                        print(f"   ❌ Data tidak ditemukan")

            except Exception as e:
                error_text = str(e)[:80]
                results[paspor] = {'Status': f'Error: {error_text}'}
                print(f"   ❌ Exception: {error_text}")

        await browser.close()
        return results


async def cek_pmi(paspor):
    """Single check - return first result"""
    results = await cek_pmi_batch([paspor])
    return results.get(paspor)


async def main():
    """CLI interface"""
    passports = sys.argv[1:] if len(sys.argv) > 1 else ['AU610053']

    print("="*60)
    print("📋 CEK STATUS PMI — BP2MI")
    print("="*60)

    results = await cek_pmi_batch(passports)

    print("\n" + "="*60)
    print("📊 HASIL CEK PMI")
    print("="*60)

    for paspor, data in results.items():
        if data and 'Status' not in data:
            nama = data.get('Nama Lengkap', data.get('Nama', '-'))
            negara = data.get('Negara Penempatan', '-')
            p3mi = data.get('P3MI/Pelaksana', data.get('P3MI', '-'))
            berlaku = data.get('Berlaku Hingga', '-')

            print(f"\n  ✅ {paspor}")
            print(f"     Nama    : {nama}")
            print(f"     Negara  : {negara}")
            print(f"     P3MI    : {p3mi}")
            print(f"     Berlaku : {berlaku}")
        else:
            status = data.get('Status', 'Unknown') if data else 'No response'
            print(f"\n  ❌ {paspor}")
            print(f"     Status: {status}")

    # Save JSON result
    with open('/tmp/hasil_pmi.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n📁 JSON hasil: /tmp/hasil_pmi.json")
    print("="*60)


if __name__ == '__main__':
    asyncio.run(main())
