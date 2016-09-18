python -m cProfile -o profile.prof test.py -n --conf 3 100 3 --input 1 2 3 && pyprof2calltree -i ./profile.prof -k
