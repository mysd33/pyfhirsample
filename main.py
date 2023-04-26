from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.resource import Resource
from fhir.resources.composition import Composition
from fhir.resources.patient import Patient
from fhir.resources.reference import Reference
from fhir.resources.humanname import HumanName
from fhir.resources.fhirtypes import String
from typing import List
import os
import pathlib
import logging

# 参考
# https://github.com/nazrulworld/fhir.resources/tree/6.2.1
# 最新のv6.2.2だとR5対応されて、R4BのみでR4サポートがなくR5になっているのでv6.2.1

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s:%(name)s - %(message)s")
  
    # 診療情報提供書のHL7 FHIRのサンプルデータを読み込み
    # Bundle-BundleReferralExample01.json    
    filename = pathlib.Path("Bundle-BundleReferralExample01.json")
    # Bundleリソースを解析    
    bundle = Bundle.parse_file(filename)
    logging.info("Bundle type: %s", bundle.type)
    # BundleからEntryを取得    
    entries: List[BundleEntry] = bundle.entry
    subjectRefId: String
    for entry in entries:
        resource: Resource = entry.resource
        resourceType = resource.resource_type
        logging.info("Resource Type: %s", resourceType)
        if resourceType == "Composition":
            # Compositionリソースを解析する例
            compostion: Composition = resource
            title = compostion.title
            logging.info("文書名: %s", title)
            # subjectの参照先のUUIDを取得
            subjectRef: Reference = compostion.subject
            subjectRefId = subjectRef.reference
            logging.info("subject display %s", subjectRef.display)
            logging.info("subject reference ID %s", subjectRefId)
            # TODO: 各参照先のUUIDを取得する処理の追加
        elif resourceType == "Patient":
            if entry.fullUrl != subjectRefId:
                continue
            logging.info("Composition.subjectの参照先のPatient: %s", subjectRefId)
            patient: Patient = resource
            # 患者番号の取得
            id = patient.identifier[0]
            logging.info("患者番号: %s", id.value)
            # 患者氏名の取得
            humanNames: List[HumanName] = patient.name
            for humanName in humanNames:
                valueCode =  humanName.extension[0].valueCode
                if valueCode == "IDE":
                    logging.info("患者氏名: %s", humanName.text)
                else:
                    logging.info("患者カナ氏名: %s", humanName.text)
        # TODO: リソース毎に処理の追加        
        
if __name__ == '__main__':
    main()