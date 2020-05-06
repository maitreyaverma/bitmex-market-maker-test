function download(){
	a='https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/quote/'
	date=$1
	full_url="${a}${date}.csv.gz"
	file_compressed="${date}.csv.gz"
	file="${date}.csv"
	axel -n 10 $full_url
	gunzip $file_compressed
	mv ${file} market_maker/backtest/data

}
function runIt(){
	filePath=market_maker/backtest/data/${1}.csv
	echo "$filePath"
	if test -f "$filePath"; then
		echo "file found"
	else
		download $1
	fi
	python runBackTest.py XBTUSD ${1}.csv>${1}
}
dates="20200301 20200302 20200303 20200304 20200305 20200306 20200307 20200308 20200309 20200310 20200311 20200312 20200313 20200314 20200315 20200316 20200317 20200318 20200319 20200320 20200321 20200322 20200323 20200324 20200325 20200326 20200327 20200328 20200329 20200330"
#dates="20200401"
for i in $dates
do
	runIt $i &
	#	./getData.sh $i &
done

