echo '=> Staring message test'
python test_text.py
sleep 4
echo '=> Staring file test'
python test_file.py
DIFF=$(diff bible.txt bible.txt.encode.decoded)
if [ "$DIFF" != "" ]
then
    echo "\033[31mRESULT => File not equals"
else
  echo "\033[92mRESULT => File equals"
fi

rm *.encode
