#!/usr/bin/env python3
"""
Test script untuk verifikasi logic captcha solving tanpa network
"""

import re


def solve_captcha(captcha_text):
    """Test fungsi pemecah captcha"""
    print(f"📝 Soal Captcha: {captcha_text}")

    try:
        match = re.match(r'(\d+)\s*([\+\-\*/])\s*(\d+)', captcha_text)

        if not match:
            print("❌ Format captcha tidak dikenali")
            return None

        num1 = int(match.group(1))
        operator = match.group(2)
        num2 = int(match.group(3))

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            result = int(num1 / num2)
        else:
            return None

        print(f"✓ Jawaban captcha: {result}")
        return str(result)

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_captcha_solving():
    """Test berbagai jenis soal captcha"""
    print("="*60)
    print("🧪 TEST CAPTCHA SOLVING LOGIC")
    print("="*60 + "\n")

    test_cases = [
        ("5 + 3", "8"),
        ("10 - 4", "6"),
        ("6 * 7", "42"),
        ("20 / 5", "4"),
        ("15 + 25", "40"),
        ("100 - 50", "50"),
        ("3 * 9", "27"),
        ("12 / 3", "4"),
    ]

    passed = 0
    failed = 0

    for captcha, expected in test_cases:
        result = solve_captcha(captcha)

        if result == expected:
            print(f"   ✓ PASS\n")
            passed += 1
        else:
            print(f"   ❌ FAIL - Expected {expected}, got {result}\n")
            failed += 1

    print("="*60)
    print(f"📊 HASIL TEST: {passed} PASS, {failed} FAIL")
    print("="*60)

    if failed == 0:
        print("\n✅ Semua test passed! Logic script OK.")
        print("\nScript siap dijalankan di komputer lokal Anda dengan:")
        print("   python3 cek_pmi.py <NOMOR_PASPOR>")
    else:
        print("\n❌ Ada test yang gagal!")


if __name__ == "__main__":
    test_captcha_solving()
