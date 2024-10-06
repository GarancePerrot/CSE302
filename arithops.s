	.section	.rodata
.lprintfmt:
	.string	"%ld\n"

	.text
	.globl	main
main:
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$144, %rsp
	movq	$42, -0(%rbp)
	movq	-0(%rbp), %r11
	movq	%r11, -8(%rbp)
	movq	$1, -16(%rbp)
	movq	-8(%rbp), %r11
	movq	-16(%rbp), %rcx
	sarq	%cl, %r11
	movq	%r11, -24(%rbp)
	movq	-0(%rbp), %r11
	movq	%r11, -32(%rbp)
	movq	-24(%rbp), %r11
	movq	%r11, -40(%rbp)
	movq	-32(%rbp), %r11
	addq	-40(%rbp), %r11
	movq	%r11, -48(%rbp)
	leaq	.lprintfmt(%rip), %rdi
	movq	-48(%rbp), %rsi
	xorq	%rax, %rax
	callq	printf@PLT
	movq	-0(%rbp), %r11
	movq	%r11, -56(%rbp)
	movq	-24(%rbp), %r11
	movq	%r11, -64(%rbp)
	movq	-56(%rbp), %r11
	subq	-64(%rbp), %r11
	movq	%r11, -72(%rbp)
	leaq	.lprintfmt(%rip), %rdi
	movq	-72(%rbp), %rsi
	xorq	%rax, %rax
	callq	printf@PLT
	movq	-0(%rbp), %r11
	movq	%r11, -80(%rbp)
	movq	$3, -88(%rbp)
	movq	-80(%rbp), %r11
	imulq	-88(%rbp)
	movq	%rax, -96(%rbp)
	movq	-24(%rbp), %r11
	movq	%r11, -104(%rbp)
	movq	-96(%rbp), %r11
	addq	-104(%rbp), %r11
	movq	%r11, -112(%rbp)
	movq	-112(%rbp), %r11
	movq	%r11, -120(%rbp)
	movq	-0(%rbp), %r11
	movq	%r11, -128(%rbp)
	movq	-120(%rbp), %r11
	cqto
	idivq	-128(%rbp)
	movq	%rdx, -136(%rbp)
	leaq	.lprintfmt(%rip), %rdi
	movq	-136(%rbp), %rsi
	xorq	%rax, %rax
	callq	printf@PLT
	movq	%rbp, %rsp
	popq	%rbp
	xorq	%rax, %rax
	retq
