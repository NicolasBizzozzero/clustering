#!/usr/bin/env bash
#
# Run the `clus` command asynchronously and quietly over multiple seeds, and
# save their results.
# Do not provide the --seed nor the --save and --quiet commands, as they are already
# provided.

NUMBER_OF_SEEDS=50

for i in $(seq 1 $NUMBER_OF_SEEDS); do
    clus $@ --seed $i --save --quiet &
done
wait
echo "All $NUMBER_OF_SEEDS process completed"
