import argparse
import configparser
import os, sys

ROOT_DIR = os.path.dirname(__file__)
CLUSTER_INI_TEMPLATE_PATH = os.path.join(ROOT_DIR, 'templates', 'cluster.ini')

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--cluster-name', default=os.environ.get('DST_SERVER_NAME')
    )
    parser.add_argument(
        '--cluster-token', default=os.environ.get('DST_CLUSTER_TOKEN')
    )
    parser.add_argument(
        '--cluster-description', default=os.environ.get('DST_CLUSTER_DESCRIPTION')
    )
    parser.add_argument(
        '--cluster-intention', default=os.environ.get('DST_CLUSTER_INTENTION')
    )
    parser.add_argument(
        '--cluster-password', default=os.environ.get('DST_CLUSTER_PASSWORD')
    )
    parser.add_argument(
        '--build-dir', default=os.path.join(os.getcwd(), 'build')
    )
    args = parser.parse_args(argv)

    name = args.cluster_name
    if not name:
        print(f'ERROR: --cluster-name not specified')
        return 1

    token = args.cluster_token
    if not token:
        print(f'ERROR: --cluster-token not specified')
        return 1
    
    desc = args.cluster_description
    if not desc:
        print(f'ERROR: --cluster-description not specified')
        return 1

    intention = args.cluster_intention
    if not intention:
        print(f'ERROR: --cluster-intention not specified')
        return 1

    password = args.cluster_password
    if not password:
        print('ERROR: --cluster-password not specified')
        return 1

    build_dir = args.build_dir
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    cfg = configparser.ConfigParser()
    cfg.read(CLUSTER_INI_TEMPLATE_PATH)
    cn = cfg['NETWORK']
    cn['cluster_name'] = name
    cn['cluster_description'] = desc
    cn['cluster_intention'] = intention
    cn['cluster_password'] = password
    
    with open(os.path.join(build_dir, 'cluster.ini'), 'w') as f:
        cfg.write(f)

    ret = os.system(f'echo "{token}" > {args.build_dir}/cluster_token.txt')
    if ret != 0:
        print('ERROR creating cluster token file')
        return 1

    



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))