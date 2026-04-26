@echo off
echo ========================================
echo Installing Packages for Python 3.12
echo ========================================
echo.

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing numpy 1.26.3...
pip install numpy==1.26.3

echo Installing pandas 2.2.0...
pip install pandas==2.2.0

echo Installing scikit-learn 1.4.1...
pip install scikit-learn==1.4.1.post1

echo Installing flask 3.0.2...
pip install flask==3.0.2

echo Installing joblib 1.3.2...
pip install joblib==1.3.2

echo.
echo ========================================
echo Verification
echo ========================================
python -c "import numpy; import pandas; import sklearn; import flask; import joblib; print('✅ Python version:', __import__('sys').version.split()[0]); print('✅ numpy:', numpy.__version__); print('✅ pandas:', pandas.__version__); print('✅ sklearn:', sklearn.__version__); print('✅ flask:', flask.__version__); print('✅ joblib:', joblib.__version__); print('\n🎉 All packages installed successfully!')"

pause