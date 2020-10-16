echo "<html>"
#tre-agrep -d"^\{" $1 ld/*/* |sed '/^ld\//s//<p>/'
agrep -d"^\{" $1 ld/*/* |sed '/^ld\//s//<p>/'
echo "</html>"
