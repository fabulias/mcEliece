echo '=> Staring message test'
python test_text.py

echo '=> Staring file test'
python test_file.py
DIFF=$(diff bible.txt bible.txt.encode.decoded)
if [ "$DIFF" != "" ]
then
    echo "RESULT => File not equals"
else
  echo "RESULT => File equals"
fi

rm *.encode
rm *.decoded
