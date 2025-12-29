---
title: Git Best Practices
---

# Git Best Practices

## Git configuration
 
## Commit Messages
- Use conventional commit format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep first line under 50 characters
- Use imperative mood ("Add feature" not "Added feature")
- Include body for complex changes

## Branching
- The global default branch name shold be setup to be `main`, `git config --global init.defaultbranch main`
- New branches on remote should be created automatically, `git config set push.autosetupremote true`
- Use feature branches for new development
- Keep main branch stable and deployable
- Use descriptive branch names (feature/user-auth, fix/login-bug)
- Delete merged branches to keep repository clean

### Branch Naming Convention

Use the format: `type/short-description`

**Branch Types:**

**Feature Development:**
- `feature/user-authentication`
- `feature/payment-integration`
- `feature/search-functionality`

**Bug Fixes:**
- `fix/login-validation-error`
- `fix/memory-leak-issue`
- `fix/broken-navigation`

**Documentation:**
- `docs/api-documentation`
- `docs/setup-guide`
- `docs/troubleshooting`

**Refactoring:**
- `refactor/database-layer`
- `refactor/component-structure`
- `refactor/error-handling`

**Testing:**
- `test/unit-tests-auth`
- `test/integration-tests`
- `test/performance-testing`

**Configuration/Infrastructure:**
- `config/ci-pipeline`
- `config/docker-setup`
- `config/environment-variables`

**Hotfixes (urgent production fixes):**
- `hotfix/critical-security-patch`
- `hotfix/payment-gateway-down`

**Experimental/Research:**
- `experiment/new-ui-framework`
- `research/performance-optimization`

**Branch Naming Best Practices:**
1. Use lowercase and hyphens (kebab-case)
2. Keep descriptions short but descriptive
3. Use present tense ("add" not "added")
4. Be specific enough to understand the purpose
5. Include ticket numbers if using issue tracking:
   - `feature/AUTH-123-user-login`
   - `fix/BUG-456-payment-error`

## Workflow
- Pull latest changes before starting work
- Commit frequently with logical chunks
- Use interactive rebase to clean up history before merging
- Review code before merging (pull requests)

## Repository Management
- Use .gitignore to exclude build artifacts and secrets
- Use .gitatributes to set default behavior to normalize line endings
- Ask questions to pair down the .gitignore and .gitattributes to just the configuration that is needed.
- Keep repository size manageable (use Git LFS for large files)
- Tag releases with semantic versioning
- Document branching strategy in README

## Security
- Never commit secrets, API keys, or passwords
- Use environment variables for configuration
- Review commits for sensitive information
- Use signed commits when possible


# Template .gitattributes configuration

```
# Set default behavior to automatically normalize line endings
* text=auto

# Explicitly declare text files with LF line endings
*.txt text eol=lf
*.md text eol=lf
*.json text eol=lf
*.xml text eol=lf
*.yaml text eol=lf
*.yml text eol=lf

# Python files - always LF
*.py text eol=lf
*.pyw text eol=lf
*.pyx text eol=lf
*.pxd text eol=lf

# Shell scripts - always LF
*.sh text eol=lf
*.bash text eol=lf
*.zsh text eol=lf

# Windows-specific files - CRLF
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf

# Binary files - no line ending conversion
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
*.zip binary
*.tar binary
*.gz binary
*.exe binary
*.dll binary
*.so binary
*.dylib binary
```

# Template .gitignore configuration

```
### Terraform ###
# Local .terraform directories
**/.terraform/*

# .tfstate files
*.tfstate
*.tfstate.*

# Crash log files
crash.log

# Ignore any .tfvars files that are generated automatically for each Terraform run. Most
# .tfvars files are managed as part of configuration and so should be included in
# version control.
#
# example.tfvars

# Ignore override files as they are usually used to override resources locally and so
# are not checked in
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Include override files you do wish to add to version control using negated pattern
#
# !example_override.tf

# Compiled source #
###################
*.com
*.class
*.dll
*.exe
*.o
*.so

# Packages #
############
# it's better to unpack these files and commit the raw source
# git has its own built in compression methods
*.7z
*.dmg
*.gz
*.iso
*.jar
*.rar
*.tar
*.zip

# Logs and databases #
######################
*.log
*.sql
*.sqlite
*.mdf
*.ldf
*.ndf

# OS generated files #
######################
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes

### Windows ###
# Windows thumbnail cache files
Thumbs.db
ehthumbs.db
ehthumbs_vista.db

# Dump file
*.stackdump

# Folder config file
[Dd]esktop.ini

# Recycle Bin used on file shares
$RECYCLE.BIN/

# Windows Installer files
*.cab
*.msi
*.msix
*.msm
*.msp

# Windows shortcuts
*.lnk

### VisualStudio ###
## Ignore Visual Studio temporary files, build results, and
## files generated by popular Visual Studio add-ons.
##
## Get latest from https://github.com/github/gitignore/blob/master/VisualStudio.gitignore

# User-specific files
*.suo
*.user
*.userosscache
*.sln.docstates

# User-specific files (MonoDevelop/Xamarin Studio)
*.userprefs

# Build results
[Dd]ebug/
[Dd]ebugPublic/
[Rr]elease/
[Rr]eleases/
x64/
x86/
bld/
[Bb]in/
[Oo]bj/
[Ll]og/

# Visual Studio 2015/2017 cache/options directory
.vs/
# Uncomment if you have tasks that create the project's static files in wwwroot
#wwwroot/

# Visual Studio 2017 auto generated files
Generated\ Files/

# MSTest test Results
[Tt]est[Rr]esult*/
[Bb]uild[Ll]og.*

# NUNIT
*.VisualState.xml
TestResult.xml

# Build Results of an ATL Project
[Dd]ebugPS/
[Rr]eleasePS/
dlldata.c

# Benchmark Results
BenchmarkDotNet.Artifacts/

# .NET Core
project.lock.json
project.fragment.lock.json
artifacts/

# StyleCop
StyleCopReport.xml

# Files built by Visual Studio
*_i.c
*_p.c
*_h.h
*.ilk
*.meta
*.obj
*.iobj
*.pch
*.pdb
*.ipdb
*.pgc
*.pgd
*.rsp
*.sbr
*.tlb
*.tli
*.tlh
*.tmp
*.tmp_proj
*_wpftmp.csproj
*.log
*.vspscc
*.vssscc
.builds
*.pidb
*.svclog
*.scc

# Chutzpah Test files
_Chutzpah*

# Visual C++ cache files
ipch/
*.aps
*.ncb
*.opendb
*.opensdf
*.sdf
*.cachefile
*.VC.db
*.VC.VC.opendb

# Visual Studio profiler
*.psess
*.vsp
*.vspx
*.sap

# Visual Studio Trace Files
*.e2e

# TFS 2012 Local Workspace
$tf/

# Guidance Automation Toolkit
*.gpState

# ReSharper is a .NET coding add-in
_ReSharper*/
*.[Rr]e[Ss]harper
*.DotSettings.user

# JustCode is a .NET coding add-in
.JustCode

# TeamCity is a build add-in
_TeamCity*

# DotCover is a Code Coverage Tool
*.dotCover

# AxoCover is a Code Coverage Tool
.axoCover/*
!.axoCover/settings.json

# Visual Studio code coverage results
*.coverage
*.coveragexml

# NCrunch
_NCrunch_*
.*crunch*.local.xml
nCrunchTemp_*

# MightyMoose
*.mm.*
AutoTest.Net/

# Web workbench (sass)
.sass-cache/

# Installshield output folder
[Ee]xpress/

# Click-Once directory
publish/

# Publish Web Output
*.[Pp]ublish.xml
*.azurePubxml
# Note: Comment the next line if you want to checkin your web deploy settings,
# but database connection strings (with potential passwords) will be unencrypted
*.pubxml
*.publishproj

# Microsoft Azure Web App publish settings. Comment the next line if you want to
# checkin your Azure Web App publish settings, but sensitive information contained
# in these scripts will be unencrypted
PublishScripts/

# NuGet Packages
*.nupkg
# The packages folder can be ignored because of Package Restore
**/[Pp]ackages/*
# except build/, which is used as an MSBuild target.
!**/[Pp]ackages/build/
# Uncomment if necessary however generally it will be regenerated when needed
#!**/[Pp]ackages/repositories.config
# NuGet v3's project.json files produces more ignorable files
*.nuget.props
*.nuget.targets

# Microsoft Azure Build Output
csx/
*.build.csdef

# Microsoft Azure Emulator
ecf/
rcf/

# Windows Store app package directories and files
AppPackages/
BundleArtifacts/
Package.StoreAssociation.xml
_pkginfo.txt
*.appx

# Visual Studio cache files
# files ending in .cache can be ignored
*.[Cc]ache
# but keep track of directories ending in .cache
!*.[Cc]ache/

# Others
ClientBin/
~$*
*~
*.dbmdl
*.dbproj.schemaview
*.jfm
*.pfx
*.publishsettings
orleans.codegen.cs

# Including strong name files can present a security risk
# (https://github.com/github/gitignore/pull/2483#issue-259490424)
#*.snk

# Since there are multiple workflows, uncomment next line to ignore bower_components
# (https://github.com/github/gitignore/pull/1529#issuecomment-104372622)
#bower_components/

# RIA/Silverlight projects
Generated_Code/

# Backup & report files from converting an old project file
# to a newer Visual Studio version. Backup files are not needed,
# because we have git ;-)
_UpgradeReport_Files/
Backup*/
UpgradeLog*.XML
UpgradeLog*.htm
ServiceFabricBackup/
*.rptproj.bak



# Business Intelligence projects
*.rdl.data
*.bim.layout
*.bim_*.settings
*.rptproj.rsuser

# Microsoft Fakes
FakesAssemblies/

# GhostDoc plugin setting file
*.GhostDoc.xml

# Node.js Tools for Visual Studio
.ntvs_analysis.dat
node_modules/

# Visual Studio 6 build log
*.plg

# Visual Studio 6 workspace options file
*.opt

# Visual Studio 6 auto-generated workspace file (contains which files were open etc.)
*.vbw

# Visual Studio LightSwitch build output
**/*.HTMLClient/GeneratedArtifacts
**/*.DesktopClient/GeneratedArtifacts
**/*.DesktopClient/ModelManifest.xml
**/*.Server/GeneratedArtifacts
**/*.Server/ModelManifest.xml
_Pvt_Extensions

# Paket dependency manager
.paket/paket.exe
paket-files/

# FAKE - F# Make
.fake/

# JetBrains Rider
.idea/
*.sln.iml

# CodeRush personal settings
.cr/personal

# Python Tools for Visual Studio (PTVS)
__pycache__/
*.pyc

# Cake - Uncomment if you are using it
# tools/**
# !tools/packages.config

# Tabs Studio
*.tss

# Telerik's JustMock configuration file
*.jmconfig

# OpenCover UI analysis results
OpenCover/

# Azure Stream Analytics local run output
ASALocalRun/

# MSBuild Binary and Structured Log
*.binlog

# NVidia Nsight GPU debugger configuration file
*.nvuser

# MFractors (Xamarin productivity tool) working folder
.mfractor/

# Local History for Visual Studio
.localhistory/

# End of https://www.gitignore.io/
```