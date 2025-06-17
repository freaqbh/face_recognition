@echo off
setlocal enabledelayedexpansion

:: Face Recognition Benchmark Usage Script for Windows
:: This script provides an easy interface to run face recognition benchmarks
:: Author: Face Recognition Benchmark Tool
:: Version: 1.0

echo.
echo ==========================================
echo  Face Recognition Benchmark Tool
echo ==========================================
echo.

:: Color definitions for better output
:: Using color codes for Windows terminal
set "COLOR_GREEN=0A"
set "COLOR_YELLOW=0E"
set "COLOR_RED=0C"
set "COLOR_BLUE=0B"
set "COLOR_RESET=07"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color %COLOR_RED%
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and add it to your PATH
    color %COLOR_RESET%
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

:: Check if benchmark.py exists
if not exist "benchmark.py" (
    color %COLOR_RED%
    echo ERROR: benchmark.py not found in current directory
    echo Please ensure benchmark.py is in the same folder as this script
    color %COLOR_RESET%
    pause
    exit /b 1
)

:: Main menu
:MAIN_MENU
cls
echo.
echo ==========================================
echo  Face Recognition Benchmark Tool
echo ==========================================
echo.
echo Choose an option:
echo.
echo [1] Setup Environment
echo [2] Quick Benchmark (Fast test with popular models)
echo [3] Full Benchmark (Comprehensive test with all models)
echo [4] Custom Benchmark (Choose specific detectors/models)
echo [5] Performance Benchmark (Balanced speed and accuracy)
echo [6] Speed Benchmark (Fastest combinations only)
echo [7] Accuracy Benchmark (Most accurate combinations)
echo [8] View Previous Results
echo [9] Clean Results Directory
echo [0] Exit
echo.
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto SETUP
if "%choice%"=="2" goto QUICK_BENCHMARK
if "%choice%"=="3" goto FULL_BENCHMARK
if "%choice%"=="4" goto CUSTOM_BENCHMARK
if "%choice%"=="5" goto PERFORMANCE_BENCHMARK
if "%choice%"=="6" goto SPEED_BENCHMARK
if "%choice%"=="7" goto ACCURACY_BENCHMARK
if "%choice%"=="8" goto VIEW_RESULTS
if "%choice%"=="9" goto CLEAN_RESULTS
if "%choice%"=="0" goto EXIT
goto MAIN_MENU

:SETUP
cls
echo.
echo ==========================================
echo  Environment Setup
echo ==========================================
echo.

:: Check if requirements file exists
if not exist "benchmark_requirements.txt" (
    echo Creating benchmark_requirements.txt...
    (
        echo # Requirements for Face Recognition Benchmarking Script
        echo # Install with: pip install -r benchmark_requirements.txt
        echo.
        echo # Core dependencies
        echo Flask
        echo deepface
        echo opencv-python-headless
        echo numpy
        echo tf-keras
        echo.
        echo # Additional dependencies for benchmarking
        echo pandas^>=1.3.0
        echo matplotlib^>=3.3.0
        echo seaborn^>=0.11.0
        echo psutil^>=5.8.0
        echo scikit-learn^>=1.0.0
        echo.
        echo # Optional: For advanced plotting
        echo plotly^>=5.0.0
        echo kaleido^>=0.2.1
        echo.
        echo # For progress bars
        echo tqdm^>=4.60.0
        echo.
        echo # For statistical analysis
        echo scipy^>=1.7.0
    ) > benchmark_requirements.txt
    echo benchmark_requirements.txt created successfully!
)

:: Install requirements
echo Installing required packages...
echo This may take several minutes...
pip install -r benchmark_requirements.txt
if %errorlevel% neq 0 (
    color %COLOR_RED%
    echo ERROR: Failed to install requirements
    color %COLOR_RESET%
    pause
    goto MAIN_MENU
)

:: Create directory structure
echo.
echo Creating benchmark directory structure...
if not exist "benchmark_data" mkdir benchmark_data
if not exist "benchmark_data\test_images" mkdir benchmark_data\test_images
if not exist "benchmark_results" mkdir benchmark_results

:: Create test data guide
echo Creating test data guide...
(
    echo # Test Data Structure Guide
    echo.
    echo Your test images should be organized as follows:
    echo.
    echo ```
    echo test_images/
    echo ├── person1/
    echo │   ├── image1.jpg
    echo │   ├── image2.jpg
    echo │   └── image3.jpg
    echo ├── person2/
    echo │   ├── image1.jpg
    echo │   └── image2.jpg
    echo ├── person3/
    echo │   ├── image1.jpg
    echo │   ├── image2.jpg
    echo │   └── image3.jpg
    echo └── ...
    echo ```
    echo.
    echo ## Guidelines:
    echo - Each person should have their own directory
    echo - Each person should have at least 2 images for genuine pair testing
    echo - Use clear, front-facing photos when possible
    echo - Supported formats: .jpg, .png
    echo - Minimum 3 different people recommended
    echo - 5-10 people with 3-5 images each is ideal for comprehensive testing
    echo.
    echo ## Preparing Your Data:
    echo 1. Create directories named after each person ^(e.g., person1, person2, etc.^)
    echo 2. Place multiple images of the same person in their respective directory
    echo 3. Ensure good image quality and proper face visibility
    echo 4. The benchmark will automatically create genuine pairs ^(same person^) and impostor pairs ^(different people^)
) > benchmark_data\README.md

color %COLOR_GREEN%
echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Add your test images to benchmark_data\test_images\
echo 2. Follow the structure guide in benchmark_data\README.md
echo 3. Run a benchmark from the main menu
color %COLOR_RESET%
echo.
pause
goto MAIN_MENU

:QUICK_BENCHMARK
cls
echo.
echo ==========================================
echo  Quick Benchmark
echo ==========================================
echo.
echo This will test popular detector-model combinations for fast results.
echo Estimated time: 5-15 minutes depending on your data size.
echo.
echo Detectors: opencv, mtcnn, retinaface
echo Models: VGG-Face, Facenet, ArcFace
echo.
call :CHECK_TEST_DATA
if %errorlevel% neq 0 goto MAIN_MENU

echo Starting quick benchmark...
python benchmark.py --test-dir "benchmark_data\test_images" --output-dir "benchmark_results\quick_benchmark_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%" --quick

call :SHOW_RESULTS
goto MAIN_MENU

:FULL_BENCHMARK
cls
echo.
echo ==========================================
echo  Full Benchmark
echo ==========================================
echo.
echo This will test ALL detector-model combinations.
echo WARNING: This can take 1-3 hours depending on your system and data size.
echo.
echo Detectors: opencv, ssd, dlib, mtcnn, retinaface, mediapipe, yolov8, yunet
echo Models: VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID, ArcFace, Dlib, SFace
echo.
call :CHECK_TEST_DATA
if %errorlevel% neq 0 goto MAIN_MENU

set /p confirm="Are you sure you want to proceed with full benchmark? (y/N): "
if /i not "%confirm%"=="y" goto MAIN_MENU

echo Starting full benchmark...
python benchmark.py --test-dir "benchmark_data\test_images" --output-dir "benchmark_results\full_benchmark_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"

call :SHOW_RESULTS
goto MAIN_MENU

:CUSTOM_BENCHMARK
cls
echo.
echo ==========================================
echo  Custom Benchmark
echo ==========================================
echo.
echo Available Detectors:
echo opencv, ssd, dlib, mtcnn, retinaface, mediapipe, yolov8, yunet
echo.
echo Available Models:
echo VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID, ArcFace, Dlib, SFace
echo.
call :CHECK_TEST_DATA
if %errorlevel% neq 0 goto MAIN_MENU

echo Enter detectors separated by spaces (or press Enter for all):
set /p custom_detectors="Detectors: "

echo Enter models separated by spaces (or press Enter for all):
set /p custom_models="Models: "

set benchmark_cmd=python benchmark.py --test-dir "benchmark_data\test_images" --output-dir "benchmark_results\custom_benchmark_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"

if not "%custom_detectors%"=="" (
    set benchmark_cmd=!benchmark_cmd! --detectors %custom_detectors%
)

if not "%custom_models%"=="" (
    set benchmark_cmd=!benchmark_cmd! --models %custom_models%
)

echo Starting custom benchmark...
%benchmark_cmd%

call :SHOW_RESULTS
goto MAIN_MENU

:PERFORMANCE_BENCHMARK
cls
echo.
echo ==========================================
echo  Performance Benchmark
echo ==========================================
echo.
echo This tests combinations balanced for speed and accuracy.
echo Estimated time: 10-30 minutes depending on your data size.
echo.
echo Detectors: opencv, mtcnn, retinaface, mediapipe
echo Models: VGG-Face, Facenet, Facenet512, ArcFace
echo.
call :CHECK_TEST_DATA
if %errorlevel% neq 0 goto MAIN_MENU

echo Starting performance benchmark...
python benchmark.py --test-dir "benchmark_data\test_images" --output-dir "benchmark_results\performance_benchmark_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%" --detectors opencv mtcnn retinaface mediapipe --models VGG-Face Facenet Facenet512 ArcFace

call :SHOW_RESULTS
goto MAIN_MENU

:SPEED_BENCHMARK
cls
echo.
echo ==========================================
echo  Speed Benchmark
echo ==========================================
echo.
echo This tests the fastest detector-model combinations.
echo Estimated time: 3-10 minutes depending on your data size.
echo.
echo Detectors: opencv, mediapipe
echo Models: VGG-Face, OpenFace
echo.
call :CHECK_TEST_DATA
if %errorlevel% neq 0 goto MAIN_MENU

echo Starting speed benchmark...
python benchmark.py --test-dir "benchmark_data\test_images" --output-dir "benchmark_results\speed_benchmark_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%" --detectors opencv mediapipe --models VGG-Face OpenFace

call :SHOW_RESULTS
goto MAIN_MENU

:ACCURACY_BENCHMARK
cls
echo.
echo ==========================================
echo  Accuracy Benchmark
echo ==========================================
echo.
echo This tests the most accurate detector-model combinations.
echo Estimated time: 10-25 minutes depending on your data size.
echo.
echo Detectors: mtcnn, retinaface
echo Models: Facenet512, ArcFace
echo.
call :CHECK_TEST_DATA
if %errorlevel% neq 0 goto MAIN_MENU

echo Starting accuracy benchmark...
python benchmark.py --test-dir "benchmark_data\test_images" --output-dir "benchmark_results\accuracy_benchmark_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%" --detectors mtcnn retinaface --models Facenet512 ArcFace

call :SHOW_RESULTS
goto MAIN_MENU

:VIEW_RESULTS
cls
echo.
echo ==========================================
echo  Previous Results
echo ==========================================
echo.

if not exist "benchmark_results" (
    echo No results directory found.
    echo Run a benchmark first to generate results.
    pause
    goto MAIN_MENU
)

echo Available result directories:
echo.
set count=0
for /d %%i in ("benchmark_results\*") do (
    set /a count+=1
    echo [!count!] %%~nxi
    set "dir!count!=%%i"
)

if %count%==0 (
    echo No benchmark results found.
    echo Run a benchmark first to generate results.
    pause
    goto MAIN_MENU
)

echo.
set /p choice="Select result directory to view (1-%count%) or 0 to go back: "

if "%choice%"=="0" goto MAIN_MENU
if %choice% gtr %count% goto VIEW_RESULTS
if %choice% lss 1 goto VIEW_RESULTS

set selected_dir=!dir%choice%!
echo.
echo Opening results directory: !selected_dir!
echo.

:: Check for different result files and open them
if exist "!selected_dir!\benchmark_report.md" (
    echo Opening benchmark report...
    start "" "!selected_dir!\benchmark_report.md"
)

if exist "!selected_dir!\benchmark_summary.csv" (
    echo Opening summary CSV...
    start "" "!selected_dir!\benchmark_summary.csv"
)

if exist "!selected_dir!\benchmark_visualizations.png" (
    echo Opening visualizations...
    start "" "!selected_dir!\benchmark_visualizations.png"
)

echo Opening results folder...
start "" "!selected_dir!"

pause
goto MAIN_MENU

:CLEAN_RESULTS
cls
echo.
echo ==========================================
echo  Clean Results Directory
echo ==========================================
echo.

if not exist "benchmark_results" (
    echo No results directory found.
    pause
    goto MAIN_MENU
)

echo This will delete ALL benchmark results.
echo This action cannot be undone.
echo.
set /p confirm="Are you sure you want to delete all results? (y/N): "

if /i not "%confirm%"=="y" goto MAIN_MENU

echo Cleaning results directory...
rmdir /s /q "benchmark_results" 2>nul
mkdir "benchmark_results"

color %COLOR_GREEN%
echo Results directory cleaned successfully!
color %COLOR_RESET%
pause
goto MAIN_MENU

:CHECK_TEST_DATA
echo Checking test data...
if not exist "benchmark_data\test_images" (
    color %COLOR_RED%
    echo ERROR: Test images directory not found
    echo Please run "Setup Environment" first and add your test images
    color %COLOR_RESET%
    pause
    exit /b 1
)

:: Count person directories
set person_count=0
for /d %%i in ("benchmark_data\test_images\*") do (
    set /a person_count+=1
)

if %person_count% lss 2 (
    color %COLOR_RED%
    echo ERROR: Not enough test data found
    echo You need at least 2 person directories with images
    echo Current person directories: %person_count%
    echo.
    echo Please check benchmark_data\README.md for data structure guide
    color %COLOR_RESET%
    pause
    exit /b 1
)

echo Found %person_count% person directories - Good to go!
echo.
exit /b 0

:SHOW_RESULTS
echo.
if %errorlevel% equ 0 (
    color %COLOR_GREEN%
    echo Benchmark completed successfully!
    color %COLOR_RESET%
    echo.
    echo Results have been saved to the benchmark_results directory.
    echo You can view them using option 8 from the main menu.
) else (
    color %COLOR_RED%
    echo Benchmark failed or was interrupted.
    color %COLOR_RESET%
    echo Check the log files for more information.
)
echo.
pause
exit /b 0

:EXIT
echo.
echo Thank you for using Face Recognition Benchmark Tool!
echo.
pause
exit /b 0

:: Function to display colored text (if needed)
:COLORED_ECHO
echo %~2
exit /b 0