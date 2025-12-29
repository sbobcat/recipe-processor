# AWS Observability 

## Cloudwatch Dashboard

```
AWSTemplateFormatVersion: '2010-09-09'
Description: 'CloudWatch Dashboard for Amazon Textract Monitoring'

Resources:
  TextractMonitoringDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: 'Textract-Monitoring-Dashboard'
      DashboardBody: !Sub |
        {
          "widgets": [
            {
              "type": "metric",
              "x": 0,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/Textract", "SuccessfulRequestCount", "Operation", "DetectDocumentText" ],
                  [ ".", ".", ".", "AnalyzeDocument" ],
                  [ ".", ".", ".", "StartDocumentAnalysis" ],
                  [ ".", ".", ".", "GetDocumentAnalysis" ],
                  [ ".", ".", ".", "StartDocumentTextDetection" ],
                  [ ".", ".", ".", "GetDocumentTextDetection" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Successful Requests by Operation",
                "period": 300,
                "stat": "Sum"
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/Textract", "UserErrorCount", "Operation", "DetectDocumentText" ],
                  [ ".", ".", ".", "AnalyzeDocument" ],
                  [ ".", ".", ".", "StartDocumentAnalysis" ],
                  [ ".", "ServerErrorCount", ".", "DetectDocumentText" ],
                  [ ".", ".", ".", "AnalyzeDocument" ],
                  [ ".", ".", ".", "StartDocumentAnalysis" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Error Counts by Operation",
                "period": 300,
                "stat": "Sum"
              }
            },
            {
              "type": "metric",
              "x": 0,
              "y": 6,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/Textract", "ResponseTime", "Operation", "DetectDocumentText" ],
                  [ ".", ".", ".", "AnalyzeDocument" ],
                  [ ".", ".", ".", "StartDocumentAnalysis" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Response Time by Operation",
                "period": 300,
                "stat": "Average"
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 6,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/Textract", "ThrottledCount", "Operation", "DetectDocumentText" ],
                  [ ".", ".", ".", "AnalyzeDocument" ],
                  [ ".", ".", ".", "StartDocumentAnalysis" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Throttled Requests by Operation",
                "period": 300,
                "stat": "Sum"
              }
            }
          ]
        }

  # CloudWatch Alarms for Textract
  HighErrorRateAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: 'Textract-High-Error-Rate'
      AlarmDescription: 'Alarm when Textract error rate is high'
      MetricName: UserErrorCount
      Namespace: AWS/Textract
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold
      TreatMissingData: notBreaching

  HighThrottleAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: 'Textract-High-Throttle-Rate'
      AlarmDescription: 'Alarm when Textract throttle rate is high'
      MetricName: ThrottledCount
      Namespace: AWS/Textract
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 5
      ComparisonOperator: GreaterThanThreshold
      TreatMissingData: notBreaching

Outputs:
  DashboardURL:
    Description: 'URL of the CloudWatch Dashboard'
    Value: !Sub 'https://${AWS::Region}.console.aws.amazon.com/cloudwatch/home?region=${AWS::Region}#dashboards:name=${TextractMonitoringDashboard}'
```

## Service Quotas

### Service Quota Dashboard

```
# Additional CloudWatch Dashboard Widget for Service Quotas
ServiceQuotaDashboard:
  Type: AWS::CloudWatch::Dashboard
  Properties:
    DashboardName: 'Textract-Service-Quotas'
    DashboardBody: !Sub |
      {
        "widgets": [
          {
            "type": "metric",
            "x": 0,
            "y": 0,
            "width": 24,
            "height": 6,
            "properties": {
              "metrics": [
                [ "AWS/Usage", "CallCount", "Type", "API", "Resource", "DetectDocumentText", "Service", "Textract", "Class", "None" ],
                [ ".", ".", ".", ".", ".", "AnalyzeDocument", ".", ".", ".", "." ],
                [ ".", ".", ".", ".", ".", "StartDocumentAnalysis", ".", ".", ".", "." ]
              ],
              "view": "timeSeries",
              "stacked": false,
              "region": "${AWS::Region}",
              "title": "API Call Usage vs Quotas",
              "period": 3600,
              "stat": "Sum"
            }
          }
        ]
      }
```

### Service Quota Alarm

```
QuotaUtilizationAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: 'Textract-Quota-Utilization-High'
    AlarmDescription: 'Alarm when Textract quota utilization is high'
    MetricName: CallCount
    Namespace: AWS/Usage
    Dimensions:
      - Name: Service
        Value: Textract
      - Name: Type
        Value: API
      - Name: Resource
        Value: DetectDocumentText
      - Name: Class
        Value: None
    Statistic: Sum
    Period: 3600
    EvaluationPeriods: 1
    Threshold: 800  # Adjust based on your quota limits
    ComparisonOperator: GreaterThanThreshold
```

## Cloudtrail Queries

### Count of Textract API calls by operation

```
fields @timestamp, eventName, sourceIPAddress, userIdentity.userName
| filter eventSource = "textract.amazonaws.com"
| stats count() by eventName
| sort count desc
```

### Textract operations with errors

```
fields @timestamp, eventName, errorCode, errorMessage, sourceIPAddress
| filter eventSource = "textract.amazonaws.com" and ispresent(errorCode)
| sort @timestamp desc
```

### Document analysis jobs started

```
fields @timestamp, eventName, requestParameters.documentLocation.s3Object.bucket, requestParameters.documentLocation.s3Object.name, responseElements.jobId
| filter eventName = "StartDocumentAnalysis"
| sort @timestamp desc
```

### Textract usage by user

```
fields @timestamp, eventName, userIdentity.userName, userIdentity.type
| filter eventSource = "textract.amazonaws.com"
| stats count() by userIdentity.userName, eventName
| sort count desc
```

## Athena

Create a CloudTrail Table

```
CREATE EXTERNAL TABLE cloudtrail_logs (
    eventversion STRING,
    useridentity STRUCT<
        type: STRING,
        principalid: STRING,
        arn: STRING,
        accountid: STRING,
        invokedby: STRING,
        accesskeyid: STRING,
        userName: STRING,
        sessioncontext: STRUCT<
            attributes: STRUCT<
                mfaauthenticated: STRING,
                creationdate: STRING>,
            sessionissuer: STRUCT<
                type: STRING,
                principalId: STRING,
                arn: STRING,
                accountId: STRING,
                userName: STRING>>>,
    eventtime STRING,
    eventsource STRING,
    eventname STRING,
    awsregion STRING,
    sourceipaddress STRING,
    useragent STRING,
    errorcode STRING,
    errormessage STRING,
    requestparameters STRING,
    responseelements STRING,
    additionaleventdata STRING,
    requestid STRING,
    eventid STRING,
    resources ARRAY<STRUCT<
        ARN: STRING,
        accountId: STRING,
        type: STRING>>,
    eventtype STRING,
    apiversion STRING,
    readonly STRING,
    recipientaccountid STRING,
    serviceeventdetails STRING,
    sharedeventid STRING,
    vpcendpointid STRING
)
PARTITIONED BY (
   region string,
   year string,
   month string,
   day string
)
STORED AS INPUTFORMAT 
  'com.amazon.emr.cloudtrail.CloudTrailInputFormat'
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://your-cloudtrail-bucket/AWSLogs/your-account-id/CloudTrail/'
```

### Athena Textract Usage patterns

```
SELECT 
    eventname,
    COUNT(*) as call_count,
    DATE(eventtime) as date
FROM cloudtrail_logs
WHERE eventsource = 'textract.amazonaws.com'
    AND year = '2024'
    AND month = '12'
GROUP BY eventname, DATE(eventtime)
ORDER BY date DESC, call_count DESC;
```

## SNS

Set up SNS notifications for alarms:

```
TextractAlertsTopicPolicy:
  Type: AWS::SNS::Topic
  Properties:
    TopicName: 'textract-monitoring-alerts'
    DisplayName: 'Textract Monitoring Alerts'
```