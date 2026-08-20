# Day 1 - Emirp Number Finder & GPIO LED Control


---

## Tasks Completed

### Task 1: Emirp Number Finder
- Developed a C program to find emirp numbers (prime numbers whose reverse is also prime, excluding palindromes) within a user-defined range [A, B]
- Implemented primality testing optimized to sqrt(n) using `<math.h>`
- Used dynamic memory allocation with `malloc` to store emirp pairs and their absolute differences
- Included input validation for positive integers and proper range (A < B)
- Displayed each emirp with its reversed counterpart and absolute difference
- Generated summary statistics: total count, largest difference, and smallest difference

### Task 2: GPIO LED Control
- Learned Raspberry Pi GPIO programming using `libgpiod` library
- Configured GPIO chip (`gpiochip0`) and pin 17 (BCM layout) as output
- Implemented LED blinking with 500ms intervals using custom delay function
- Resolved compilation issues by linking `-lgpiod` flag
- Created `gcall()` bash function to automate compilation with proper library flags (`-lm`, `-lgpiod`, `-lpthread`)

---

## Key Learnings
- Prime number algorithms and optimization techniques
- Dynamic memory management in C using structs and malloc/free
- GPIO control on Raspberry Pi using modern `libgpiod` interface
- Library linking during compilation and bash scripting for automation
- Input validation and error handling in C

---

## Tools & Technologies
- **Languages:** C
- **Libraries:** stdio.h, stdlib.h, math.h, gpiod.h
- **Hardware:** Raspberry Pi 4
- **Build Tools:** GCC, pkg-config
- **Version Control:** Git/GitHub

---

## Files Created
- `task1.c` - Emirp number finder program
- `led_blink.c` - GPIO LED blinking program
- `gcall()` - Bash function for automated compilation

---

## Challenges & Solutions
- **Issue:** Compilation failed due to missing `-lgpiod` flag
- **Solution:** Created bash function to automatically detect required libraries using `pkg-config` and grep

---

## Next Steps
- Implement timer interrupts for non-blocking LED control
- Add button input to interact with LED behavior
