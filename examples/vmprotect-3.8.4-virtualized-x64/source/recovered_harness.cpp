// REU self-owned VMProtect benchmark. No network, persistence, or external data.
// A passing self-test proves behavior only; it does NOT detect unpacking.
#include <windows.h>
#include <stdint.h>

// Core implementation is generated from the protected native trace, not this source.
extern "C" uint32_t ReuRecoveredTransform(uint32_t);
extern "C" __declspec(dllexport) __declspec(noinline)
uint32_t ReuChallengeTransform(uint32_t x) { return ReuRecoveredTransform(x); }

static const char* find(const char* text, const char* needle) {
    for (; *text; ++text) {
        const char* a = text;
        const char* b = needle;
        while (*a && *b && *a == *b) { ++a; ++b; }
        if (!*b) return text;
    }
    return nullptr;
}

static void print(const char* text) {
    DWORD count = 0, written = 0;
    while (text[count]) ++count;
    WriteFile(GetStdHandle(STD_OUTPUT_HANDLE), text, count, &written, nullptr);
}

static void print_number(uint32_t value) {
    char buffer[11];
    unsigned pos = 10;
    buffer[pos] = 0;
    do { buffer[--pos] = char('0' + value % 10); value /= 10; } while (value);
    print(buffer + pos);
}

extern "C" void entry() {
    const char* command = GetCommandLineA();
    const char* value_arg = find(command, "--value ");
    if (value_arg) {
        const char* cursor = value_arg + 8;
        while (*cursor == ' ') ++cursor;
        uint32_t value = 0;
        if (*cursor < '0' || *cursor > '9') ExitProcess(2);
        while (*cursor >= '0' && *cursor <= '9') {
            const uint32_t digit = uint32_t(*cursor++ - '0');
            if (value > 429496729u || (value == 429496729u && digit > 5)) ExitProcess(2);
            value = value * 10 + digit;
        }
        if (*cursor && *cursor != ' ' && *cursor != '"') ExitProcess(2);
        print_number(ReuChallengeTransform(value));
        print("\r\n");
        ExitProcess(0);
    }
    // Expected values were calculated with an independent Python implementation.
    const uint32_t inputs[] = {0u, 1u, 2u, 42u, 123456789u, 0x80000000u, 0xfffffffeu, 0xffffffffu};
    const uint32_t expected[] = {2912250588u, 2454535933u, 765757648u, 2807516844u,
        2673263555u, 919905649u, 3347589262u, 3298643878u};
    unsigned passed = 0;
    for (unsigned i = 0; i < 8; ++i) {
        if (ReuChallengeTransform(inputs[i]) == expected[i]) ++passed;
    }
    if (find(command, "--negative-test")) passed = 0;
    const bool success = passed == 8;
    print("REU / recovered native-function harness\r\n");
    print(success ? "FUNCTIONAL SELF-TEST: PASS (8/8)\r\n" : "FUNCTIONAL SELF-TEST: FAIL\r\n");
    print("A passing self-test does not prove unpacking or devirtualization.\r\n");
    if (find(command, "--show")) {
        MessageBoxW(nullptr,
            success ? L"功能自检成功：8 / 8\n\n此结果只证明程序功能正常。\n脱壳状态由外部验证器判定。"
                    : L"功能自检失败。\n退出码：1",
            L"REU | VMProtect 3.8.4 benchmark", MB_OK | (success ? MB_ICONINFORMATION : MB_ICONERROR));
    }
    ExitProcess(success ? 0 : 1);
}
