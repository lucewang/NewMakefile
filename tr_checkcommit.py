import gitlab
import argparse
import subprocess
import os
import sys
import re
from datetime import datetime
from urllib import quote

# GitLab API configuration
GITLAB_URL = 'https://gitlabe1.ext.net.nokia.com'  # Update with your GitLab URL
GITLAB_TOKEN = '2wtY6dsFnu5Xas7BUDw2'  # Update with your GitLab access token
PROJECT_ID = '63330'  # Update with your project ID
LAST_COMMIT_FILE = 'last_commit.txt'  # File to store the last checked commit ID
RESULT_FILE = 'result.txt' # File to store the result
SPECIFIC_FILENAME = 'common/' # Update with the specific filename to filter
MAKEFILE_FILENAME = '/weixw_repo/nbn_target/BBDFWA_Appsrc/Mgnt/OAMCore/tr069_ms/Makefile'
OUTPUT_FILE = 'build_output.txt'  # File to save the command output
LOG_DIR = '/weixw_repo/logs/trCommon/'

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Check for new commit IDs with the specific filename on a branch.')
parser.add_argument('branch', help='Name of the branch to check')
parser.add_argument('product', help='Name of the product to check')
args = parser.parse_args()

if args.branch == "master":
    if args.product == "WNTD4":
        MAKEFILE_FILENAME = '/weixw_repo/nbn_target/BBDFWA_Appsrc/Mgnt/OAMCore/tr069_ms/Makefile'
        CURRENT_DIR = '/weixw_repo/nbn_target/BBDFWA_Appsrc/Mgnt/OAMCore/tr069_ms/'
        COVERITY_DIR = '/weixw_repo/nbn_target/tr069Common/tr069_FWA/' 
    elif args.product == "5GGW3-OMNI-1":
        MAKEFILE_FILENAME = '/weixw_repo/target_repo/BBDFWA_Appsrc/Mgnt/OAMCore/tr069_ms/Makefile'
        CURRENT_DIR = '/weixw_repo/target_repo/BBDFWA_Appsrc/Mgnt/OAMCore/tr069_ms/'
        COVERITY_DIR = '/weixw_repo/target_repo/tr069Common/tr069_FWA/' 
    else:
        print("input invalid product name!(WNTD4/5GGW3-OMNI-1/...)")
        sys.exit(0)
elif args.branch == "BBD_R2302":        
    if args.product == "WNTD4":
        MAKEFILE_FILENAME = '/weixw_repo/2302_repo/BBDFWA_Appsrc/Mgnt/OAMCore/tr069_ms/Makefile'
        CURRENT_DIR = '/weixw_repo/2302_repo/BBDFWA_Appsrc/Mgnt/OAMCore/tr069_ms/'
        COVERITY_DIR = '/weixw_repo/2302_repo/tr069Common/tr069_FWA/' 
    else:
        print("input invalid product name!(WNTD4/...)")
        sys.exit(0)
else:
    print("input invalid branch name!(master/BBD_R2302/...)")
    sys.exit(0)

print('current project diretory: ' + CURRENT_DIR)

# Create GitLab client
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)

# Get the project
project = gl.projects.get(PROJECT_ID)

LAST_COMMIT_FILE = LOG_DIR + args.branch + '_' + args.product + '_' + LAST_COMMIT_FILE

# Read the last checked commit ID
try:
    with open(LAST_COMMIT_FILE, 'a+') as file:
        last_commit = file.read().strip()
except FileNotFoundError:
    last_commit = None

# Get the branch
#branch = project.branches.get(BRANCH_NAME)
branch = project.branches.get(args.branch)

# Get the commits
#commits = project.commits.list(all=True)
# Get the commits on the branch
commits = project.commits.list(ref_name=branch.name, all=True)

# Check for new commit IDs and filter for the specific filename
new_commits = []
for commit in commits:
    if commit.id == last_commit:
        break
    commit_diff = project.commits.get(commit.id).diff()
    for diff in commit_diff:
        if SPECIFIC_FILENAME in diff.get('new_path'):
            new_commits.append(commit.id)
            break

# Update the last checked commit ID
#if commits and last_commit != commits[0].id:
#    with open(LAST_COMMIT_FILE, 'w') as file:
#        file.write(commits[0].id)

RESULT_FILE = LOG_DIR + args.branch + '_' + args.product + '_' + RESULT_FILE
currentDateAndTime = datetime.now()
currentTime = currentDateAndTime.strftime("%Y-%m-%d %H:%M:%S")
currentDate = currentDateAndTime.strftime("%Y-%m-%d")
file = open(RESULT_FILE, 'a+')
file.seek(0)
file.truncate()
file.write(currentTime)
file.write('\n')

# Print the result
if new_commits:
    result_output = "New commit IDs with the specific filename found:"
    print(result_output)
    file.write(result_output)
    file.write('\n')
    #file = open(RESULT_FILE, 'a')
    #file.seek(0)
    #file.truncate()
    for commit_id in new_commits:
        print(commit_id)
        file.write(commit_id)
        file.write('\n')
    #with open(SPECIFIC_FILENAME, 'r+') as file:
    #    content = file.read()
    #    for commit_id in new_commits:
    #        content = content.replace(last_commit, commit_id)
    #    file.seek(0)
    #    file.write(content)
    #    file.truncate()
    #file.close()

else:
    result_output = "No new commit IDs with the specific filename."
    print(result_output)
    file.write(result_output)

#file.close()

OUTPUT_FILE = LOG_DIR + args.branch + '_' + args.product + '_' + OUTPUT_FILE

# Function to run a Linux command and capture the execution status
def run_command(command,directory):
    try:
        #subprocess.check_call(command, shell=True, cwd="/weixw_repo/nbn_branch/BBDFWA_Appsrc/Mgnt/OAMCore/tr069_ms/")
        process = subprocess.Popen(command, shell=True, cwd=CURRENT_DIR,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        with open(OUTPUT_FILE, 'a+') as file:
            file.write(stdout.decode('utf-8'))
            file.write(stderr.decode('utf-8'))

        failure_messages = ["Error 2", "Build failed", "[ERROR]"]
        # Check for specific failures or errors
        for failure_message in failure_messages:
            if failure_message in stderr.decode("utf-8"):
                print("Failure occurred:", failure_message)
                return False

        return True
        #if stderr is not None and stderr.strip() != "":
        #    return False
        #else:
        #    return True  # Command executed successfully
    except subprocess.CalledProcessError:
        return False  # Command execution failed

try:
    os.remove(OUTPUT_FILE)
except OSError:
    pass

def sendemail(content):
    myemail = "wei.xb.wang@nokia-sbell.com,pu.a.zhou@nokia-sbell.com,yaxiang.chen@nokia-sbell.com,yueping.zhou@nokia-sbell.com,heming.a.tang@nokia-sbell.com"
    #myemail = "wei.xb.wang@nokia-sbell.com"
    subject = "tr069Common Compile Report (" + args.branch + "/" + args.product + ") -- " + currentDate
    #not support attachment now
    #attachment_paths = ["master_5GGW3-OMNI-1_result.txt", "master_5GGW3-OMNI-1_build_output.txt"]
    
    # Escape special characters in the subject and content
    escaped_subject = quote(subject)
    escaped_content = quote(content)

    # Substitute variable values in the URL
    url = (
        "http://135.251.205.171:8090/job/SendMail/buildWithParameters"
        "?Recipient_List={0}&Subject={1}&Content={2}"
    ).format(myemail, escaped_subject, escaped_content)

    # Construct the curl command
    #command = "curl -X POST '{0}' --data-urlencode token=GoodboywillnotsendmaiL".format(url)
    command = "curl -X POST '{0}' --form-string token=GoodboywillnotsendmaiL".format(url)

    # Append attachments to the curl command
    #for attachment_path in attachment_paths:
    #    command += " --form attachment=@{0}".format(attachment_path)
        
    # Execute the command without waiting for its completion
    subprocess.Popen(command, shell=True)

    #following use for debug
    #process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout, stderr = process.communicate()
    #print("stdout:", stdout)
    #print("stderr:", stderr)

def replaceCommitid(commitid):
    # Replace the previous commit ID with the new commit ID in the specific file using sed
    #if new_commits:
    #for commit_id in new_commits:
    print("Replaced the previous commit ID with the new commit ID in the specific file -- " + commitid)
    #subprocess.call(['sed', '-i', 's/{}/{}/g'.format(last_commit, commits[0].id), MAKEFILE_FILENAME])

    # Read the content of the file
    make_file = open(MAKEFILE_FILENAME, 'r')
    content = make_file.read()
    make_file.close()

    # Replace the desired line
    pattern = r'PKG_SOURCE_COMMITID = .+'  # Pattern to match " PKG_SOURCE_COMMITID = " followed by any characters
    new_line = 'PKG_SOURCE_COMMITID = ' +  commitid # New line to replace the matched line
    print(new_line)
    modified_content = re.sub(pattern, new_line, content)

    # Write the modified content back to the file
    make_file = open(MAKEFILE_FILENAME, 'w')
    make_file.write(modified_content)
    make_file.close()

if commits and last_commit != commits[0].id:
    # Update the last checked commit ID
    #with open(LAST_COMMIT_FILE, 'w') as filecommit:
    #    filecommit.write(commits[0].id)

    # Replace the previous commit ID with the new commit ID in the specific file using sed
    replaceCommitid(commits[0].id)

    isTerminal = False
    # Example usage: Run a Linux command in a specific directory and check if it succeeded or failed
    command = "make clean"
    print(command)
    file.write(command)
    file.write('\n')
    success = run_command(command,CURRENT_DIR)
    if success:
        result_output = 'make clean successful. pls see ' + OUTPUT_FILE
    else:
        result_output = 'make clean failed. pls see ' + OUTPUT_FILE
        isTerminal = True
    result_output += '\n'
    print(result_output)
    file.write(result_output)
    email_content = result_output

    if isTerminal:
        sendemail(email_content)
        file.close()
        sys.exit(0)
    
    command = "make product=" + args.product
    print(command)
    file.write(command)
    file.write('\n')
    success = run_command(command,CURRENT_DIR)
    if success:
        result_output = 'build tr069common successful. pls see ' + OUTPUT_FILE
    else:
        result_output = 'build tr069common failed. pls see ' + OUTPUT_FILE
        isTerminal = True
    result_output += '\n'
    print(result_output)
    file.write(result_output)
    email_content += result_output 
    if isTerminal:
        sendemail(email_content)
        file.close()
        sys.exit(0)

    # Update the last checked commit ID
    with open(LAST_COMMIT_FILE, 'w') as filecommit:
        filecommit.write(commits[0].id)

    #run coverity
    command = "DOMAIN=OAM run_coverity.sh " + args.product
    print(command)
    file.write(command)
    file.write('\n')
    success = run_command(command,COVERITY_DIR)
    if success:
        result_output = 'coverity running successful. pls see ' + OUTPUT_FILE
    else:
        result_output = 'coverity running failed. pls see ' + OUTPUT_FILE
    print(result_output)
    file.write(result_output)
    email_content += result_output

    #send email
    sendemail(email_content)

file.close()
