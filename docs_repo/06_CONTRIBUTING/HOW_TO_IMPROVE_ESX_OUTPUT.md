# How To Improve ESX Output

## Start In The Right Place

ESX output work belongs primarily in:

- `src/pdf_to_esx_agent/export/esx_writer.py`
- `src/pdf_to_esx_agent/export/validator.py`
- `src/pdf_to_esx_agent/models/estimate.py` when the canonical contract must expand

## Recommended Process

1. confirm whether the missing information already exists in the canonical estimate
2. if not, add it to the canonical model and parser first
3. update the XML writer
4. update validation rules if the structure changes
5. add or update tests
6. document the new mapping in `docs_repo/04_MAPPING_AND_FORMATS/`

## Evidence Levels

| Change type | Evidence expectation |
| --- | --- |
| add more canonical fields into existing XML sections | moderate |
| strengthen package validation | moderate |
| change XML structure | strong |
| change package contents | strong |
| attempt native proprietary packing | very strong |

The stronger the compatibility claim, the stronger the evidence should be from real ESX references.

## Safe Changes

- adding more canonical fields into existing sections
- expanding manifest metadata
- strengthening validation rules
- refining numeric formatting or text omission rules

## Higher-Risk Changes

- changing root structure
- changing `SUMMARY_REF` behavior
- changing package contents
- attempting a native proprietary packer

## Related Docs

- [../02_ARCHITECTURE/ESX_GENERATION_FLOW.md](../02_ARCHITECTURE/ESX_GENERATION_FLOW.md)
- [../04_MAPPING_AND_FORMATS/CANONICAL_TO_ESX_MAPPING.md](../04_MAPPING_AND_FORMATS/CANONICAL_TO_ESX_MAPPING.md)
- [../04_MAPPING_AND_FORMATS/XML_ESX_ASSUMPTIONS.md](../04_MAPPING_AND_FORMATS/XML_ESX_ASSUMPTIONS.md)
