README.md: FORCE
	cat README.md | sed '/^There .* currently .* for this task.$$/,$$d' > temp.md
	/usr/bin/python3 eval.py >> temp.md
	mv temp.md $@

clean:
	rm -Rf predictions

distclean:
	make clean
	rm -Rf datasets models

FORCE:
