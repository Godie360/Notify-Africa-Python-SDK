#!/usr/bin/env python3
"""
Deployment preparation script for Notify Africa Python SMS SDK
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a required file exists"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ Missing {description}: {file_path}")
        return False

def check_directory_structure():
    """Check that all required directories and files exist"""
    print("🔍 Checking directory structure...")
    
    required_files = [
        ("setup.py", "Setup script"),
        ("README.md", "README file"),
        ("LICENSE", "License file"),
        ("requirements.txt", "Requirements file"),
        ("MANIFEST.in", "Manifest file"),
        ("CHANGELOG.md", "Changelog"),
        ("CONTRIBUTING.md", "Contributing guidelines"),
        ("notify_africa/__init__.py", "Package init"),
        ("notify_africa/client.py", "Main client"),
        ("notify_africa/exceptions.py", "Exceptions"),
        ("notify_africa/models.py", "Data models"),
        ("notify_africa/utils.py", "Utilities"),
        ("tests/__init__.py", "Tests init"),
        ("tests/test_client.py", "Client tests"),
        ("tests/test_utils.py", "Utils tests"),
        ("example.py", "Main example"),
        ("sms_status_examples.py", "Status examples")
    ]
    
    all_exist = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_package_imports():
    """Check that the package can be imported correctly"""
    print("\n📦 Checking package imports...")
    
    try:
        import notify_africa
        print(f"✅ Package import successful")
        print(f"✅ Version: {notify_africa.__version__}")
        
        from notify_africa import NotifyAfricaClient
        print(f"✅ NotifyAfricaClient import successful")
        
        from notify_africa.exceptions import (
            AuthenticationError,
            ValidationError,
            InsufficientCreditsError,
            NetworkError
        )
        print(f"✅ Exception imports successful")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def run_basic_tests():
    """Run basic functionality tests"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test phone number validation
        from notify_africa.utils import normalize_phone_number, validate_phone_numbers
        
        test_number = normalize_phone_number("0712345678")
        if test_number == "255712345678":
            print("✅ Phone number normalization works")
        else:
            print(f"❌ Phone normalization failed: {test_number}")
            return False
        
        # Test client initialization
        from notify_africa import NotifyAfricaClient
        client = NotifyAfricaClient(api_key="test", sender_id="test")
        print("✅ Client initialization works")
        
        return True
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False

def check_version_consistency():
    """Check that version is consistent across files"""
    print("\n🔢 Checking version consistency...")
    
    # Get version from __init__.py
    init_version = None
    with open("notify_africa/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                init_version = line.split("=")[1].strip().strip('"').strip("'")
                break
    
    # Get version from setup.py
    setup_version = None
    with open("setup.py", "r") as f:
        for line in f:
            if "version=" in line and not line.strip().startswith("#"):
                setup_version = line.split("version=")[1].split(",")[0].strip().strip('"').strip("'")
                break
    
    if init_version and setup_version and init_version == setup_version:
        print(f"✅ Version consistent: {init_version}")
        return True
    else:
        print(f"❌ Version mismatch - __init__.py: {init_version}, setup.py: {setup_version}")
        return False

def clean_build_artifacts():
    """Clean any build artifacts"""
    print("\n🧹 Cleaning build artifacts...")
    
    artifacts = [
        "build/",
        "dist/",
        "*.egg-info/",
        "__pycache__/",
        "**/__pycache__/",
        "*.pyc",
        "**/*.pyc"
    ]
    
    import glob
    import shutil
    
    for pattern in artifacts:
        for path in glob.glob(pattern, recursive=True):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"🗑️  Removed directory: {path}")
                else:
                    os.remove(path)
                    print(f"🗑️  Removed file: {path}")
            except Exception as e:
                print(f"⚠️  Could not remove {path}: {e}")

def build_package():
    """Build the package"""
    print("\n🔨 Building package...")
    
    try:
        # Build source distribution
        result = subprocess.run([sys.executable, "setup.py", "sdist"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Source distribution built successfully")
        else:
            print(f"❌ Source build failed: {result.stderr}")
            return False
        
        # Build wheel distribution
        result = subprocess.run([sys.executable, "setup.py", "bdist_wheel"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Wheel distribution built successfully")
        else:
            print("⚠️  Wheel build failed (wheel may not be installed)")
        
        return True
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def check_readme():
    """Check README file quality"""
    print("\n📖 Checking README...")
    
    try:
        with open("README.md", "r") as f:
            content = f.read()
        
        required_sections = [
            "# Notify Africa Python SMS SDK",
            "## Installation",
            "## Quick Start",
            "## Usage Examples",
            "## Features"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if not missing_sections:
            print(f"✅ README has all required sections")
            print(f"✅ README length: {len(content)} characters")
            return True
        else:
            print(f"❌ Missing README sections: {missing_sections}")
            return False
            
    except Exception as e:
        print(f"❌ README check failed: {e}")
        return False

def generate_deployment_report():
    """Generate a deployment readiness report"""
    print("\n" + "="*60)
    print("📋 DEPLOYMENT READINESS REPORT")
    print("="*60)
    
    checks = [
        ("Directory Structure", check_directory_structure),
        ("Package Imports", check_package_imports),
        ("Basic Functionality", run_basic_tests),
        ("Version Consistency", check_version_consistency),
        ("README Quality", check_readme)
    ]
    
    results = {}
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}:")
        results[check_name] = check_func()
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 READY FOR DEPLOYMENT!")
        print("\nNext steps:")
        print("1. git add . && git commit -m 'Prepare for v1.0.0 release'")
        print("2. git tag v1.0.0")
        print("3. git push origin main --tags")
        print("4. twine upload dist/*")
        return True
    else:
        print("\n⚠️  NOT READY FOR DEPLOYMENT")
        print("Please fix the failing checks before deploying.")
        return False

def main():
    """Main deployment preparation function"""
    print("🚀 Notify Africa Python SMS SDK - Deployment Preparation")
    print("="*60)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Clean artifacts first
    clean_build_artifacts()
    
    # Run all checks
    ready = generate_deployment_report()
    
    if ready:
        print("\n🔨 Building package for deployment...")
        build_success = build_package()
        
        if build_success:
            print("\n✅ Package built successfully!")
            print("\nBuilt files:")
            if os.path.exists("dist"):
                for file in os.listdir("dist"):
                    print(f"  📦 dist/{file}")
        else:
            print("\n❌ Package build failed!")
    
    return ready

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)