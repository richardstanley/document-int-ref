"""
This code sample shows Prebuilt US Personal Tax operations with the Azure AI Document Intelligence client library. 
The async versions of the samples require Python 3.8 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
endpoint = "YOUR_FORM_RECOGNIZER_ENDPOINT"
key = "YOUR_FORM_RECOGNIZER_KEY"
filepath = "YOUR_FILE_PATH"

document_intelligence_client  = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

with open(filepath, "rb") as f:
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-tax.us", body=f
    )
ustaxes = poller.result()

for idx, document in enumerate(ustaxes.documents):
    print("--------Recognizing document #{}--------".format(idx + 1))

    doc_type = document.doc_type
    if doc_type:
        print("Document Type: {}".format(doc_type))
    
    tax_year = document.fields.get("TaxYear")
    if tax_year:
        print(
            "Tax Year: {} has confidence: {}".format(
                tax_year.value_string, tax_year.confidence
            )
        )
    
    w2_copy = document.fields.get("W2Copy")
    if w2_copy:
        print(
            "W-2 Copy: {} has confidence: {}".format(
                w2_copy.value_string, w2_copy.confidence
            )
        )
    
    wages = document.fields.get("WagesTipsAndOtherCompensation")
    if wages:
        print(
            "Wages, Tips, and Other Compensation: {} has confidence: {}".format(
                wages.value_number, wages.confidence
            )
        )
    
    federal_income_tax = document.fields.get("FederalIncomeTaxWithheld")
    if federal_income_tax:
        print(
            "Federal Income Tax Withheld: {} has confidence: {}".format(
                federal_income_tax.value_number, federal_income_tax.confidence
            )
        )
    
    social_security_wages = document.fields.get("SocialSecurityWages")
    if social_security_wages:
        print(
            "Social Security Wages: {} has confidence: {}".format(
                social_security_wages.value_number, social_security_wages.confidence
            )
        )
    
    medicare_tax_withheld = document.fields.get("MedicareTaxWithheld")
    if medicare_tax_withheld:
        print(
            "Medicare Tax Withheld: {} has confidence: {}".format(
                medicare_tax_withheld.value_number, medicare_tax_withheld.confidence
            )
        )
    
    employee_info = document.fields.get("Employee")
    if employee_info:
        print("Employee Information:")
        employee_name = employee_info.value_object.get("Name")
        if employee_name:
            print(
                "  Name: {} has confidence: {}".format(
                    employee_name.value_string, employee_name.confidence
                )
            )
        employee_ssn = employee_info.value_object.get("SocialSecurityNumber")
        if employee_ssn:
            print(
                "  SSN: {} has confidence: {}".format(
                    employee_ssn.value_string, employee_ssn.confidence
                )
            )
        employee_address = employee_info.value_object.get("Address")
        if employee_address:
            print(
                "  Address: {} has confidence: {}".format(
                    employee_address.value_address, employee_address.confidence
                )
            )
    
    employer_info = document.fields.get("Employer")
    if employer_info:
        print("Employer Information:")
        employer_name = employer_info.value_object.get("Name")
        if employer_name:
            print(
                "  Name: {} has confidence: {}".format(
                    employer_name.value_string, employer_name.confidence
                )
            )
        employer_id = employer_info.value_object.get("IdNumber")
        if employer_id:
            print(
                "  ID Number: {} has confidence: {}".format(
                    employer_id.value_string, employer_id.confidence
                )
            )
        employer_address = employer_info.value_object.get("Address")
        if employer_address:
            print(
                "  Address: {} has confidence: {}".format(
                    employer_address.value_address, employer_address.confidence
                )
            )
    
    state_tax_infos = document.fields.get("StateTaxInfos")
    if state_tax_infos:
        print("State Tax Information:")
        for state_idx, state_info in enumerate(state_tax_infos.value_array):
            state = state_info.value_object.get("State")
            if state:
                print(
                    "  State #{}: {} has confidence: {}".format(
                        state_idx + 1, state.value_string, state.confidence
                    )
                )
            state_income_tax = state_info.value_object.get("StateIncomeTax")
            if state_income_tax:
                print(
                    "    State Income Tax: {} has confidence: {}".format(
                        state_income_tax.value_number, state_income_tax.confidence
                    )
                )
    
    additional_info = document.fields.get("AdditionalInfo")
    if additional_info:
        print("Additional Information:")
        for info_idx, info in enumerate(additional_info.value_array):
            letter_code = info.value_object.get("LetterCode")
            amount = info.value_object.get("Amount")
            if letter_code and amount:
                print(
                    "  Info #{}: Code: {}, Amount: {} with confidence: {}".format(
                        info_idx + 1, letter_code.value_string, amount.value_number, letter_code.confidence
                    )
                )
    
    print("--------------------------------------")
