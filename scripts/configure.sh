ROOT_DIR=`dirname $(readlink -m $0)`
cd $ROOT_DIR/../config
python -m tinytuya scan
python -m tinytuya wizard