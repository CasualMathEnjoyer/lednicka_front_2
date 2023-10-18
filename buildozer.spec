name: CI
on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Use Node.js 16
        uses: actions/setup-node@v2
        with:
          node-version: 16

      - uses: actions/checkout@v2

#      - name: Remove .extraheader from git config
#        run: |
#          if git config --global --get http.https://github.com/.extraheader; then
#            git config --global --unset http.https://github.com/.extraheader
#          fi
#
#      - name: Install Android SDK
#        run: |
#          wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip -O android-sdk.zip
#          unzip -q android-sdk.zip -d $HOME/android-sdk
#          export ANDROID_HOME=$HOME/android-sdk
#          export PATH=$PATH:$ANDROID_HOME/tools/bin
#
#      - name: Accept Android SDK licenses
#        run: yes | sdkmanager --licenses

      # used to cache dependencies with a timeout
      - name: Get Date
        id: get-date
        run: echo "date=$(date -u "+%Y%m%d")" >> $GITHUB_ENV

      - name: Cache Buildozer global directory
        uses: actions/cache@v2
        with:
          path: .buildozer_global
          key: buildozer-global-${{ hashFiles('buildozer.spec') }} # Replace with your path

      - uses: actions/cache@v2
        with:
          path: .buildozer
          key: ${{ runner.os }}-${{ steps.get-date.outputs.date }}-${{ hashFiles('buildozer.spec') }}

      - name: Build with Buildozer
        run: |
          pip3 install --user --upgrade buildozer Cython virtualenv
          export PATH=$PATH:~/.local/bin/
          export APP_ANDROID_ACCEPT_SDK_LICENSE=1
          export BUILDOZER_WARN_ON_ROOT=0
          sudo apt update
          sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
          cd ${{ github.workspace }}
          buildozer android debug
          
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          command: buildozer android debug
          buildozer_version: master

      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: package
          path: ${{ steps.buildozer.outputs.filename }}
