pytest -s -v  --cov-report xml:coverage.xml --cov=./src ./tests
sed -i 's+filename="+filename="src/+g' coverage.xml
# force to not recognize the path so that scanner will use relative path in prepare step
sed -i 's+$(Build.Repository.LocalPath)+/dummy+g' coverage.xml
