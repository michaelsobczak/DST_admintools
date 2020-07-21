import argparse
import configparser
import os, sys
import shutil

ROOT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')
CLUSTER_INI_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'cluster.ini')
CAVES_TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, 'Caves')
MASTER_TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, 'Master')

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

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)

    # make the cluster.ini file
    cfg = configparser.ConfigParser()
    cfg.read(CLUSTER_INI_TEMPLATE_PATH)
    cn = cfg['NETWORK']
    cn['cluster_name'] = name
    cn['cluster_description'] = desc
    cn['cluster_intention'] = intention
    cn['cluster_password'] = password
    
    with open(os.path.join(build_dir, 'cluster.ini'), 'w') as f:
        cfg.write(f)

    # write the secret cluster token to right file
    ret = os.system(f'echo "{token}" > {args.build_dir}/cluster_token.txt')
    if ret != 0:
        print('ERROR creating cluster token file')
        return 1

    # copy the master and caves directories to build
    shutil.copytree(CAVES_TEMPLATE_DIR, os.path.join(build_dir, 'Caves'))
    shutil.copytree(MASTER_TEMPLATE_DIR, os.path.join(build_dir, 'Master'))
    
    # delete the mod shit for now
    os.remove(os.path.join(build_dir, 'Caves', 'modoverrides.lua'))
    os.remove(os.path.join(build_dir, 'Master', 'modoverrides.lua'))

    server_name_dir = build_dir.replace(' ', '').strip()
    # build the docker image
    ret = os.system(f'docker build -t dst_admintools/gameserver:latest --build-arg SERVER_NAME="{server_name_dir}" .')
    if ret != 0:
        print('ERROR building docker image')
        return 1

    


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))