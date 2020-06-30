# AWS-Toolbox


In this repo, we provide a set off scripts that helps to manage amazon ec2 instances on your personal computers.


## Install Prerequisites

To run this these scripts you need to install the following dependencies:

1. **Amazon Command Line Interface (aws-cli):** This package provides a unified command line interface to Amazon Web Services. The aws-cli package works on Python versions `3.7.x and greater`.


### MacOS

The following steps show how to install or update to the latest version of the AWS CLI version 2 by using the standard macOS user interface and your browser. If you are updating to the latest version, use the same installation method that you used for your current version.
In your browser, download the macOS pkg file: <https://awscli.amazonaws.com/AWSCLIV2.pkg>. Double-click the downloaded file to launch the installer. Follow the on-screen instructions.


### Linux

Follow these steps from the command line to install the AWS CLI on Linux.

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```


You can install without sudo if you specify directories that you already have write permissions to. Use the following instructions for the install command to specify the installation location:

Ensure that the paths you provide to the -i and -b parameters contain no volume name or directory names that contain any space characters or other white space characters. If there is a space, the installation fails.

* --install-dir or -i – This option specifies the directory to copy all of the files to. The default value is /usr/local/aws-cli.

* --bin-dir or -b – This option specifies that the main aws program in the install directory is symbolically linked to the file aws in the specified path. You must have write permissions to the specified directory. Creating a symlink to a directory that is already in your path eliminates the need to add the install directory to the user's $PATH variable.
The default value is /usr/local/bin.

```bash
./awscli-bundle/install -b ~/bin/aws
```

Verify that the AWS CLI installed correctly.

```bash
aws --version
```

## Configure your aws


To configure your aws account on your local machine you can ask your AWS **Root User** to give you access key ID information or create a separate one for you. After getting either root information or your own specific user information follow the following steps:
```
aws configure
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [us-east-1]:
Default output format [json]:
```

Please make sure your output default format is `json`.

If you successfully configure your aws command line after running the following command you should be able to get a json file that describe details of all your instances on aws:


```bash
aws ec2 describe-instances
```

