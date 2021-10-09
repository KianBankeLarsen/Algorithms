# Algorithm: Recursive Fibonacci.
# Overall Time Complexity: O(2^n).
# Space Complexity: O(n).
# Author: https://www.linkedin.com/in/kilar.

.globl fib
.type fib, @function

fib:
    # Base case {
    cmpq $2, %rdi       # rdi < 2
    jl .endFib
    # }
    # First fib call {
    decq %rdi           # Call fib n-1
    push %rdi           # Save RDI to second call
    call fib            # Make the call
    popq %rdi           # Restore RDI to second call
    # }
    push %rax           # Save recursive base case on stack
    # Second fib call {
    decq %rdi           # Call fib n-2
    call fib            # Make the call
    # }
    # Accumulate result {
    popq %r8            # Put base case in %r8 before adding
    addq %r8, %rax      # Add all base cases before returning    
    # }
    jmp .return

.endFib:
    movq %rdi, %rax     # Add last base case to accumulator 
.return:
    ret
