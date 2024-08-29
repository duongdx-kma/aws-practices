const AWS = require('aws-sdk');

// config the environment
AWS.config.update({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: 'ap-southeast-1' // change your region
});

// create STS object
const sts = new AWS.STS();

async function assumeRole() {
  try {
    const assumeRoleResponse = await sts.assumeRole({
      RoleArn: 'arn:aws:iam::<Account-ID>:role/S3ReadOnlyRole',
      RoleSessionName: 's3ReadOnlySession'
    }).promise();

    // get temporary credential
    const tempCredentials = {
      accessKeyId: assumeRoleResponse.Credentials.AccessKeyId,
      secretAccessKey: assumeRoleResponse.Credentials.SecretAccessKey,
      sessionToken: assumeRoleResponse.Credentials.SessionToken
    };

    const s3 = new AWS.S3(tempCredentials);

    // list S3 bucket
    const buckets = await s3.listBuckets().promise();
    console.log('Buckets:', buckets);

  } catch (err) {
    console.error('Error assuming role:', err);
  }
}

assumeRole();
