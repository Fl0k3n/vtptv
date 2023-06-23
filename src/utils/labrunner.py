import sys

from Kathara.manager.Kathara import Kathara
from Kathara.parser.netkit.LabParser import LabParser

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'expected absolute lab path'
    lab_path = sys.argv[1]
    lab_name = '___TEST___'
    kathara = Kathara.get_instance()
    try:
        lab = LabParser().parse('lab_path')
        lab.name = lab_name
        kathara.deploy_lab(lab)
    except Exception as e:
        print(e)
        kathara.undeploy_lab(lab_name=lab_name)
        print('try again')
