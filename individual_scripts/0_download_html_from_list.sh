#!/bin/bash -xvi
main(){
  URL_list="educause_agenda_url_list.csv"
  index=1
  previous_year=""

  cat ${URL_list} | while read line; do
    year=`echo $line | awk -F, '{print $1}'`
    url=`echo $line | awk -F, '{print $2}'`

    if [[ "$year" != "$previous_year" ]]; then
      index=1
      previous_year=$year
    fi

    dir="html_${year}"
    mkdir -p $dir
    ./html_content_saver.py -u $url -o ${dir}/educause${year}_agenda_contents_${index}.html

    index=$((index+1))
    sleep 5
  done
}


main $@
