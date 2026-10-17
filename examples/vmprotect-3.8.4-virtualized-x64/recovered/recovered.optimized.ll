; ModuleID = '<string>'
source_filename = "tritonModule"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc"

; Function Attrs: mustprogress nofree norecurse nosync nounwind willreturn memory(none)
define i32 @ReuRecoveredTransform(i32 %SymVar_0) local_unnamed_addr #0 {
entry:
  %0 = xor i32 %SymVar_0, -1640531527
  %1 = zext i32 %0 to i64
  %2 = mul nuw i64 %1, 4294967297
  %3 = lshr i64 %2, 27
  %.neg = mul i64 %3, 2246822507
  %4 = add i64 %.neg, 3266489909
  %5 = and i64 %4, 4294967295
  %6 = xor i64 %5, 2671344829
  %7 = mul nuw i64 %6, 4294967297
  %8 = lshr i64 %7, 27
  %9 = mul i64 %8, 2048144789
  %10 = add i64 %9, 1028477386
  %11 = and i64 %10, 4294967295
  %12 = xor i64 %11, 1606713406
  %13 = mul nuw i64 %12, 4294967297
  %14 = lshr i64 %13, 27
  %15 = mul i64 %14, 2048144789
  %16 = add i64 %15, 1028477386
  %17 = and i64 %16, 4294967295
  %18 = xor i64 %17, 1589804346
  %19 = mul nuw i64 %18, 4294967297
  %20 = lshr i64 %19, 27
  %21 = mul i64 %20, 2048144789
  %22 = add i64 %21, 1028477386
  %23 = and i64 %22, 4294967295
  %24 = xor i64 %23, 1572895286
  %25 = mul nuw i64 %24, 4294967297
  %26 = lshr i64 %25, 27
  %.neg1 = mul i64 %26, 2246822507
  %27 = add i64 %.neg1, 3266489909
  %28 = and i64 %27, 4294967295
  %29 = xor i64 %28, 2738981069
  %30 = mul nuw i64 %29, 4294967297
  %31 = lshr i64 %30, 27
  %32 = mul i64 %31, 2048144789
  %33 = add i64 %32, 1028477386
  %34 = and i64 %33, 4294967295
  %35 = xor i64 %34, 1539077166
  %36 = mul nuw i64 %35, 4294967297
  %37 = lshr i64 %36, 27
  %38 = trunc i64 %37 to i32
  %.neg2 = mul i32 %38, -2048144789
  %39 = add i32 %.neg2, -1028477387
  ret i32 %39
}

attributes #0 = { mustprogress nofree norecurse nosync nounwind willreturn memory(none) }
