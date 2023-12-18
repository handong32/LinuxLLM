wget -r -l1 -H -t1 -N --no-parent --random-wait --wait 3 --no-http-keep-alive -A.tar.gz -erobots=off --no-check-certificate https://mirrors.edge.kernel.org/pub/linux/kernel/v2.3/
wget -r -l1 -H -t1 -N --no-parent --random-wait --wait 3 --no-http-keep-alive -A.tar.gz -erobots=off --no-check-certificate https://mirrors.edge.kernel.org/pub/linux/kernel/v2.4/
wget -r -l1 -H -t1 -N --no-parent --random-wait --wait 3 --no-http-keep-alive -A.tar.gz -erobots=off --no-check-certificate https://mirrors.edge.kernel.org/pub/linux/kernel/v2.5/
wget -r -l1 -H -t1 -N --no-parent --random-wait --wait 3 --no-http-keep-alive -A.tar.gz -erobots=off --no-check-certificate https://mirrors.edge.kernel.org/pub/linux/kernel/v2.6/
wget -r -l1 -H -t1 -N --no-parent --random-wait --wait 3 --no-http-keep-alive -A.tar.gz -erobots=off --no-check-certificate https://mirrors.edge.kernel.org/pub/linux/kernel/v3.0/
wget -r -l1 -H -t1 -N --no-parent --random-wait --wait 3 --no-http-keep-alive -A.tar.gz -erobots=off --no-check-certificate https://mirrors.edge.kernel.org/pub/linux/kernel/v3.x/
wget -r -l1 -H -t1 -N --no-parent --random-wait --wait 3 --no-http-keep-alive -A.tar.gz -erobots=off --no-check-certificate https://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/
wget -r -l1 -H -t1 -N --no-parent --random-wait --wait 3 --no-http-keep-alive -A.tar.gz -erobots=off --no-check-certificate https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/
wget -r -l1 -H -t1 -N --no-parent --random-wait --wait 3 --no-http-keep-alive -A.tar.gz -erobots=off --no-check-certificate https://mirrors.edge.kernel.org/pub/linux/kernel/v6.x/

#
wget -r -l0 -np -t1 -N --random-wait --wait 3 --no-http-keep-alive -erobots=off --no-check-certificate https://www.kernel.org/doc/Documentation/

#lwn
wget --no-check-certificate https://lwn.net/Archives/GuestIndex/
while IFS= read -r line; do wget --random-wait --wait 3 --no-http-keep-alive --no-check-certificate $line; done < articles.txt
