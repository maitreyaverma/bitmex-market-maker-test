dates="20200301 20200302 20200303 20200304 20200305 20200306 20200307 20200308 20200309 20200310 20200311 20200312 20200313 20200314 20200315 20200316 20200317 20200318 20200319 20200320 20200321 20200322 20200323 20200324 20200325 20200326 20200327 20200328 20200329 20200330" 
for i in $dates
do
	cat $i | grep "net value" | tr -dc '0-9'
	echo ",$i"
done
