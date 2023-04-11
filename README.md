## Home Assistant Addon: S3 Auto Backup

This add-on for Home Assistant allows you to create backups of your Home Assistant configuration and upload them to an Amazon S3 bucket. You can set a schedule for the backups to run using a cron-like input.

# Prerequisites

Before using this add-on, you need to have an Amazon S3 account and a bucket created. You'll also need the following information:
- Access key ID
- Secret access key
- Bucket name


# Installation

To install this add-on, follow these steps:

1. Open the Home Assistant web interface
2. Click on the Settings tab
3. Click on Add-ons
4. Click on Add-on Store
5. Open the menu on the top right and click on Repositories
6. Add the following URL to the input field: https://github.com/MerzSebastian/hassio-S3AutoBackup
7. Click on the "Add" button
8. Find the Modbus MQTT Bridge Addon and click on it
9. Click on the "Install" button


# Configuration

The following settings are required for the add-on to work properly:

- access_key_id: Your Amazon S3 access key ID
- secret_access_key: Your Amazon S3 secret access key
- bucket_name: The name of the S3 bucket to upload the backups to
- cron: A cron-like expression to schedule the backups (e.g. 0 1 * * * for daily backups at 1am)
- backup_password: A password to encrypt the backup files (optional, but recommended)
- delete_local_backup_after_upload: Whether to delete the local backup file after uploading it to S3 (default: false)

# Usage

Once you've configured the add-on, it will automatically create backups of your Home Assistant configuration based on the schedule you specified. The backups will be encrypted using the password you provided (if any), and uploaded to the S3 bucket you specified.


You can check the add-on's logs to see when the backups were created and uploaded, as well as any errors that may have occurred.

  
# Support

If you have any issues or feature requests, please open an issue on the GitHub repository.
