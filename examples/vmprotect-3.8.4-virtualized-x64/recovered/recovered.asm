	.def	@feat.00;
	.scl	3;
	.type	0;
	.endef
	.globl	@feat.00
@feat.00 = 0
	.file	"tritonModule"
	.def	ReuRecoveredTransform;
	.scl	2;
	.type	32;
	.endef
	.text
	.globl	ReuRecoveredTransform
	.p2align	4
ReuRecoveredTransform:
	xorl	$-1640531527, %ecx
	movq	%rcx, %rax
	shlq	$32, %rax
	orq	%rcx, %rax
	shrq	$27, %rax
	imull	$-2048144789, %eax, %ecx
	addl	$-1028477387, %ecx
	movabsq	$4294967297, %rax
	leaq	-1623622468(%rax), %rdx
	xorq	%rcx, %rdx
	movq	%rdx, %rcx
	shlq	$32, %rcx
	orq	%rdx, %rcx
	shrq	$27, %rcx
	imull	$2048144789, %ecx, %ecx
	addl	$1028477386, %ecx
	xorq	$1606713406, %rcx
	movq	%rcx, %rdx
	shlq	$32, %rdx
	orq	%rcx, %rdx
	shrq	$27, %rdx
	imull	$2048144789, %edx, %ecx
	addl	$1028477386, %ecx
	xorq	$1589804346, %rcx
	movq	%rcx, %rdx
	shlq	$32, %rdx
	orq	%rcx, %rdx
	shrq	$27, %rdx
	imull	$2048144789, %edx, %ecx
	addl	$1028477386, %ecx
	xorq	$1572895286, %rcx
	movq	%rcx, %rdx
	shlq	$32, %rdx
	orq	%rcx, %rdx
	shrq	$27, %rdx
	imull	$-2048144789, %edx, %ecx
	addl	$-1028477387, %ecx
	addq	$-1555986228, %rax
	xorq	%rcx, %rax
	movq	%rax, %rcx
	shlq	$32, %rcx
	orq	%rax, %rcx
	shrq	$27, %rcx
	imull	$2048144789, %ecx, %eax
	addl	$1028477386, %eax
	xorq	$1539077166, %rax
	movq	%rax, %rcx
	shlq	$32, %rcx
	orq	%rax, %rcx
	shrq	$27, %rcx
	imull	$-2048144789, %ecx, %eax
	addl	$-1028477387, %eax
	retq

