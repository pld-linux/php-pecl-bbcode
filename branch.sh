#!/bin/sh
set -e
svn=http://svn.php.net/repository/pecl/bbcode
tag=RELEASE_1_0_2
out=branch.diff

d=$-
filter() {
	set -$d
	# remove revno's for smaller diffs
	sed -e 's,^\([-+]\{3\} .*\)\t(revision [0-9]\+)$,\1,'
}

old=$svn/tags/$tag
new=$svn/trunk
echo >&2 "Running diff: $old -> $new"
LC_ALL=C svn diff --old=$old --new=$new | filter > $out.tmp

if cmp -s $out{,.tmp}; then
	echo >&2 "No new diffs..."
	rm -f $out.tmp
	exit 0
fi
mv -f $out{.tmp,}
