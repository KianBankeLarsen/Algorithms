CC 		= gcc
CFLAGS 	= -Wall -Wextra -fsanitize=address -fsanitize=leak -fsanitize=undefined
DEPS 	= cycleDetection.h Graph.h LinkedList.h
OBJ 	= main.o cycleDetection.o Graph.o LinkedList.o

# Rule for making object files.
#	Recompiles c-file if header-file is changed (dependency).
%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

# Compiles detectCycles.
detectCycles: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

# Removes executable and associated object files.
.PHONY: clean
clean:
	rm *.o detectCycles