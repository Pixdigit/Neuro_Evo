python -m cProfile -o profile.prof ./test.py --compo --nets 100 --config 1 0 1 --input 1 --seed 2 --gens 64 && pyprof2calltree -i ./profile.prof -k
