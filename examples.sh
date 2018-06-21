#!/usr/bin/env bash


# It takes a kind of stupid amount of times to run.
# Provide the script an argument which is the amt of times to run through translation.

echo "Example text undergoing 5 runs of the script:"
TEXT="This is the text that will be translated multiple times, lol!"
echo $TEXT
for (( i = 1; i <= 5; i++ )); do
  echo -n "$i. "
  py make_nonsense.py "$TEXT" 5 en
done
#!/bin/sh
