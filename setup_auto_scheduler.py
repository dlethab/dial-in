#!/usr/bin/env python3
"""
Setup script for Dialin Auto Phrase Scheduler
Helps configure and start the automated phrase scheduler.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_project_path():
    """Get the current project directory"""
    return Path(__file__).parent.absolute()

def setup_macos():
    """Setup auto-scheduler for macOS using launchd"""
    project_path = get_project_path()
    username = os.getenv('USER')
    
    # Read the plist template
    plist_path = project_path / 'com.dialin.phrasescheduler.plist'
    with open(plist_path, 'r') as f:
        plist_content = f.read()
    
    # Replace placeholders
    plist_content = plist_content.replace('YOUR_USERNAME', username)
    plist_content = plist_content.replace('/Users/YOUR_USERNAME/Desktop/dialin', str(project_path))
    
    # Write to user's LaunchAgents directory
    launch_agents_dir = Path.home() / 'Library' / 'LaunchAgents'
    launch_agents_dir.mkdir(exist_ok=True)
    
    final_plist_path = launch_agents_dir / 'com.dialin.phrasescheduler.plist'
    with open(final_plist_path, 'w') as f:
        f.write(plist_content)
    
    print(f"✅ Created launchd service at: {final_plist_path}")
    
    # Load the service
    try:
        subprocess.run(['launchctl', 'load', str(final_plist_path)], check=True)
        print("✅ Auto-scheduler service loaded and started!")
        print("📝 The service will automatically restart if it crashes")
        print("📝 Logs will be written to: phrase_scheduler.log")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to load service: {e}")
        return False
    
    return True

def setup_linux():
    """Setup auto-scheduler for Linux using systemd"""
    project_path = get_project_path()
    username = os.getenv('USER')
    
    # Read the service template
    service_path = project_path / 'dialin-phrase-scheduler.service'
    with open(service_path, 'r') as f:
        service_content = f.read()
    
    # Replace placeholders
    service_content = service_content.replace('YOUR_USERNAME', username)
    service_content = service_content.replace('/path/to/your/dialin/project', str(project_path))
    
    # Write to systemd user directory
    systemd_user_dir = Path.home() / '.config' / 'systemd' / 'user'
    systemd_user_dir.mkdir(parents=True, exist_ok=True)
    
    final_service_path = systemd_user_dir / 'dialin-phrase-scheduler.service'
    with open(final_service_path, 'w') as f:
        f.write(service_content)
    
    print(f"✅ Created systemd service at: {final_service_path}")
    
    # Enable and start the service
    try:
        subprocess.run(['systemctl', '--user', 'enable', 'dialin-phrase-scheduler.service'], check=True)
        subprocess.run(['systemctl', '--user', 'start', 'dialin-phrase-scheduler.service'], check=True)
        print("✅ Auto-scheduler service enabled and started!")
        print("📝 The service will automatically start on boot")
        print("📝 Logs can be viewed with: journalctl --user -u dialin-phrase-scheduler.service")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start service: {e}")
        return False
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import schedule
        print("✅ schedule library is installed")
        return True
    except ImportError:
        print("❌ schedule library not found")
        print("Installing schedule library...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'schedule'], check=True)
            print("✅ schedule library installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install schedule library")
            return False

def test_scheduler():
    """Test the scheduler to make sure it works"""
    print("🧪 Testing auto-scheduler...")
    try:
        result = subprocess.run([
            sys.executable, 'auto_phrase_scheduler.py', '--check-now'
        ], capture_output=True, text=True, check=True)
        print("✅ Auto-scheduler test successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Auto-scheduler test failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Dialin Auto Phrase Scheduler")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Setup failed due to missing dependencies")
        return
    
    # Test the scheduler
    if not test_scheduler():
        print("❌ Setup failed due to scheduler test failure")
        return
    
    # Setup based on platform
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("🍎 Detected macOS - setting up with launchd")
        if setup_macos():
            print("\n🎉 Setup complete! Your auto-scheduler is now running.")
            print("\n📋 Useful commands:")
            print("  • Check status: launchctl list | grep dialin")
            print("  • View logs: tail -f phrase_scheduler.log")
            print("  • Stop service: launchctl unload ~/Library/LaunchAgents/com.dialin.phrasescheduler.plist")
        else:
            print("❌ Setup failed")
    
    elif system == "Linux":
        print("🐧 Detected Linux - setting up with systemd")
        if setup_linux():
            print("\n🎉 Setup complete! Your auto-scheduler is now running.")
            print("\n📋 Useful commands:")
            print("  • Check status: systemctl --user status dialin-phrase-scheduler.service")
            print("  • View logs: journalctl --user -u dialin-phrase-scheduler.service -f")
            print("  • Stop service: systemctl --user stop dialin-phrase-scheduler.service")
        else:
            print("❌ Setup failed")
    
    else:
        print(f"❌ Unsupported operating system: {system}")
        print("You can still run the scheduler manually with:")
        print("  python3 auto_phrase_scheduler.py")

if __name__ == "__main__":
    main() 