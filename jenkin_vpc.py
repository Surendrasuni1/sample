import boto3
import sys

region=sys.argv[1]
accesskey=sys.argv[2]
secretkey=sys.argv[3]


client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)

def CreateVPC():
    response = client.create_vpc(
        CidrBlock='10.16.0.0/16',
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'ITC_VPC'
                    },
                ]
            },
        ]
    )

    Vpc_Id =(response['Vpc']['VpcId'])
    print("VPC Created successfully",Vpc_Id)
    return (Vpc_Id)

def CreateSubnet01(Vpc_Id):
    Sub_response01 = client.create_subnet(
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'ITC_Subnet_01'
                    },
                ]
            },
        ],
        AvailabilityZone='us-west-2a',
        CidrBlock='10.16.1.0/24',
        VpcId=Vpc_Id
    )
    Subnet_ID_01=Sub_response01['Subnet'][ 'SubnetId']
    print('Subnet01 Created Successfully',Subnet_ID_01)
    return(Subnet_ID_01)

def CreateSubnet02(Vpc_Id):
    Sub_response02 = client.create_subnet(
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'ITC_Subnet_02'
                    },
                ]
            },
        ],
        AvailabilityZone='us-west-2b',
        CidrBlock='10.16.2.0/24',
        VpcId=Vpc_Id
    )
    Subnet_ID_02=Sub_response02['Subnet'][ 'SubnetId']
    print('Subnet Created Successfully',Subnet_ID_02)
    return(Subnet_ID_02)
##create gateway
def CreateInternetGateway():
    internet_gateway_response = client.create_internet_gateway()
    internet_gateway_ID=internet_gateway_response['InternetGateway']['InternetGatewayId'];
    print("internet_gateway created successfully", internet_gateway_ID);
    return(internet_gateway_ID)

##attach vpc to igw
def AttachVPCIGW(internet_gateway_ID,Vpc_Id):    
    attach_vpc_IGW = client.attach_internet_gateway(InternetGatewayId=internet_gateway_ID, VpcId=Vpc_Id);
    print("internet_gateway attached successfully")

##create route table
def CreateRouteTable(Vpc_Id):
    route_table_response= client.create_route_table(
     VpcId=Vpc_Id,
        TagSpecifications=[
            {
                'ResourceType': 'route-table',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'ITC_Route_Table'
                    },
                ]
            },
        ]
    )
    routetable_ID=route_table_response['RouteTable']['RouteTableId']
    print("Routetable created successfully",routetable_ID)
    return routetable_ID

##response = client.associate_route_table(
#  DryRun=True|False,
 #   RouteTableId='string',
def CreateRoute(internet_gateway_ID,routetable_ID):
    response = client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=internet_gateway_ID,
        RouteTableId=routetable_ID,
    )


def RouteTableAssociation(sub,routetable_ID):

    for i in sub:

        route_table_association = client.associate_route_table(SubnetId=i,RouteTableId=routetable_ID)
        print(route_table_association[ 'AssociationId'])
        print("associated")
        #print("associated")
        #route_table_association = client.associate_route_table(
        #   SubnetId=Subnet_ID_02,
        #   RouteTableId=routetable_ID
        #
def main():
    print("Let created VPC setup by boto3")
    vpcid= CreateVPC()
    subnetid01=  CreateSubnet01(vpcid)
    subnetid02=CreateSubnet02(vpcid)
    internetgatewayid=CreateInternetGateway()
    AttachVPCIGW(internetgatewayid,vpcid)
    routetableid=CreateRouteTable(vpcid)
    CreateRoute(internetgatewayid,routetableid)
    sub=[subnetid01,subnetid02]
    RouteTableAssociation(sub,routetableid)

main()


        
             