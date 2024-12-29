#!/bin/bash
main(){
    file="keyword_count.csv"
    csv_output > $file
}

csv_output(){
    echo 'Year,AI,genAI,Dx'
    for year in {2000..2024}; do
        AI_count=`AI_counter $year`
        GenAI_count=`GenAI_counter $year`
        Dx_word_count=`Dx_word_counter $year`
        echo "$year,$AI_count,$GenAI_count,$Dx_word_count"
    done
}

AI_counter(){
    year=$1
    python3 AI_word_counter.py --scope title_and_content --skip-duplicates html_${year} \
    | grep html | wc | awk '{print $1}'
}

GenAI_counter(){
    year=$1
    python3 GenAI_word_counter.py --scope title_and_content --skip-duplicates html_${year} \
    | grep html | wc | awk '{print $1}'
}

Dx_word_counter(){
    year=$1
    python3 Dx_word_counter.py --scope title_and_content --skip-duplicates html_${year} \
    | grep html | wc | awk '{print $1}'
}

main "$@"
