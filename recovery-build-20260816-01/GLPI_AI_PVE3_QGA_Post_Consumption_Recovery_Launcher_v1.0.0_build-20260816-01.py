#!/usr/bin/env python3
import base64, hashlib, json, os, pathlib, socket, sys, time
TASK='task-01M015TF70VH1ECE62YXRJ38NW';TARGET_BUILD='build-20260815-06';RECOVERY_BUILD='build-20260816-01';DECISION='decision-GLPI-AI-PVE3-QGA-POST-CONSUMPTION-RECOVERY-V1-20260815';DECISION_SHA='7fa7bdec08a080e2184ab3b53424c267d73e63f57a6b1600a583412aad7d1a67';APPROVAL_SHA='39fa560d51ea04bd83f6b0887f9a29e7cd41fb43a5585955eeefd90ceaf65047';PVE3_SHA='a5d4cb9b01705c3e6d33d1d394568a401aafcff27b59be4aab06b06c4b9b9939';CAPSULE_SHA='361f0b3ae4c39aa8c278afa66d506260023827c16d8614048343476b37884b34';PAYLOAD_SHA='86c0e707b5e9679ba49a8ab5c9e59ab90bf8717e65cfa6068b8a4e2b07c388d9';AUTH_SHA='d08962a666f0e131096403b37497bbf8a807d6e3640cc6640ee7429c955b2a5c';INSTALLER_SHA='bef325ada842393c3c2e10e3bb959bcbbef644ee126aa4b612b93c6e697d52c8';RECOVERY_SHA='5bb6d411477acc24d93e817a1d11021470e9446102725a029e384d368e0cb10c'
RECOVERY_BYTES=base64.b64decode('IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwppbXBvcnQgYmFzZTY0LCBoYXNobGliLCBpbywganNvbiwgb3MsIHBhdGhsaWIsIHB3ZCwgc2h1dGlsLCBzdWJwcm9jZXNzLCBzeXMsIHRhcmZpbGUsIHVybGxpYi5wYXJzZSwgdXJsbGliLnJlcXVlc3QsIHVybGxpYi5lcnJvcgpUQVNLPSd0YXNrLTAxTTAxNVRGNzBWSDFFQ0U2MllYUkozOE5XJwpUQVJHRVRfQlVJTEQ9J2J1aWxkLTIwMjYwODE1LTA2JwpSRUNPVkVSWV9CVUlMRD0nYnVpbGQtMjAyNjA4MTYtMDEnCkRFQ0lTSU9OPSdkZWNpc2lvbi1HTFBJLUFJLVBWRTMtUUdBLVBPU1QtQ09OU1VNUFRJT04tUkVDT1ZFUlktVjEtMjAyNjA4MTUnCkRFQ0lTSU9OX1NIQT0nN2ZhN2JkZWMwOGEwODBlMjE4NGFiM2I1MzQyNGMyNjdkNzNlNjNmNTdhNmIxNjAwYTU4MzQxMmFhZDdkMWE2NycKQVBQUk9WQUxfU0hBPSczOWZhNTYwZDUxZWEwNGJkODNmNmIwODg3ZjlhMjllN2NkNDFmYjQzYTU1ODU5NTVlZWVmZDkwY2VhZjY1MDQ3JwpDQVBTVUxFX1NIQT0nMzYxZjBiM2FlNGMzOWFhOGMyNzhhZmE2NmQ1MDYyNjAwMjM4MjdjMTZkODYxNDA0ODM0MzQ3NmIzNzg4NGIzNCcKUEFZTE9BRF9TSEE9Jzg2YzBlNzA3YjVlOTY3OWJhNDlhOGFiNWM5ZTU5YWI5MGJmODcxN2U2NWNmYTYwNjhiOGE0ZTJiMDdjMzg4ZDknCkFVVEhfU0hBPSdkMDg5NjJhNjY2ZjBlMTMxMDk2NDAzYjM3NDk3YmJmOGE4MDdkNmUzNjQwY2M2NjQwZWU3NDI5Yzk1NWIyYTVjJwpJTlNUQUxMRVJfU0hBPSdiZWYzMjVhZGE4NDIzOTNjM2MyZTEwZTNiYjk1OWJjYmJlZjY0NGVlMTI2YWE0YjYxMmI5M2M2ZTY5N2Q1MmM4JwpQQVlMT0FEX0JZVEVTPWJhc2U2NC5iNjRkZWNvZGUoJ0g0c0lBQUFBQUFBQy8rMTllWC9iUnBMby9LMVB3WGplTHNnWXBBRHdKZ2N6ajVab214Tlowa3EwWTQraXhRK254SWdrYUFEVVlhKysrNnZxQStnR1FFcEtuR1BmaURPeFNLRFA2dXJxcXVvNlR0K09qSGJuOVAyNzAwWnltL3psTi9sbzhPbTBXdVF2ZlBKL20zcXJ5Ny9UNTdxbWRadC9xV2gvK1IwKzZ6aXhJK2orTC8rZW42RFg3SFcwdHRNTytyN3Z0UTNQYzN5M2E5aWRWclBiN3VwYXkrdTNIYU5yZUoyTzIydHFibURydldiZmJydU9ydnRRbElKeHdqQ0prOGhlV2JicitxdkVYcnArWTNXMzQvaEIwMmpibnQxckdjMSswMjI2aHE5cmZ0TngrdTIrNHpyd0hwREM5M1dqWTlzdHA2TWJEcFRxK0oxK0Y4Ymg5c1NXWjB0WXBmbmNqN0JoemRVN3ZXYW5xL3R1dTluVm01clJiTUZ3bTlCQ3E5OXkybmFyNTNlN3ZtMDNuVTdQdGUyZzFRNDZMb3plMEoydTB3a3FGVGRjQnJPTHhzOXh1Tnp4MjkxTzErazVmcSt2dDZDb0czUU1wKzIzTzIybjZibUc0ZW10anRGeGZjUFJ2WGJMOTJEK1FSZCt1ZEJQWHpPOFN1Vml2cHBaOXN4eTFyTzVSNGZZOHQyVzAvUzdIYnRwMkc0N3NEdDkxOUNEbnE1NXZhNFI2SjdXNnZUN1hYalViaHBldStzSC9hYmY5QUFlYlZmcnRudFpvMjdrZS80eW1kbnpHQnUyMjdCZ1JzOEpQSy9WZFhTbjVmUzlaa3Z2NjNyZ3c2TDEzS0N0Ry9EUmcyNmcyN1pyYTA3WDZMczlXM2Q3WGtjVEd2YWkyYlZ2QVhTWDhTcU1FbXk4M1RZNjNaYlg3am45Zmw5djI3Ylgxb3lXcDJsdUIwYW13YkowamFiV0RPeVdaamY5ZnREMGZCOVF3KzU1aUJYdGZ0YjRiT241SzMrSkk3Y3U3SVRpZytHNmZRTmI5elNqNzhDaUdSNDg2TGlPYjdzZFYzZjBqcWI1TGNBUXU2a0hXbGZ2ZDlzd2s4RFFBdGNIZk10YUQ2RnBCTTE4QnUwVHFQUjdNTGhtcjlWc2R6WEEwMTVQQzd5ZzArMDZkcy9RUFpoU0s5RDBqcUhiQUdLdkYzaU8zblBiT2tERTlUdUc3UXROUis2bGp6aVhoR1FoZTNaWGQ5czlWOU1kdDlNMWV0MWVxMlUzUFFjQTBtKzJXN2J0T0UyOXE4RmlBRDYyRGIwTmlOeXkvVzdmYmJtdTA3R3psbGZoZk9iZVdmN3lZcllrOEdoM3ZGYXpyd0V5ZFpyOVRxL1hCMEFFdnViWVJ0OXZ0bG93MXNEMnZDNUFDRUFONDNVQmdJN1hOd3piNkxVMEx4Q2FocVdjemYwTDM3T2k5WExKVUZCdjloeERoNDFyQS93QVY1czkyelZzWGRkZ013SitkSndnc052ZG50M3h1N0NWWGEzbE8wN0xjd1BmNzhKcUNwZ1MyMHZQQ1creFVRQkFxOTNyYTEwWWJxZnZlQWhQSFZxeCswSGIwNE9tYnZkZ3B3SEdOWTArUUtnRjJPSzNEYnZwYXJiUmFqZjFyTkdiTUxxS1Y3WUxLQmlHRkxkYmdOWU83Sm1XclFNMUFIclQxSHB0d0xGQTY4Q21zYkZEZ0tqV0N6UkFlS2RsMkYzYmE4RStoR24yREVDYlNtVmhMMmNCTEIvZDJZWUxHNlZyZDd0SUVaeCtwd3VJMjNPTmpoN0FabW43UUlsYW5VRDNQUmhyRy9DbHIvdUFpTDJ1MjNOaEJXRkhWaXF4UHc4U2JBOUcxK242bXVlMERWL3JlMTBmU0pqWENRQ05XMEc3MDlNZEkvQmMzd002NnZVNnVDdWJRUTlnNlFPU2U3MTJ0Mms3TVBYNExrNzhoYmVMSUtqYnM3cXdTZXBrazhSK2REMXovUjBQUm96SXJHdEJ4ek8wRG42Nm1tSDBEYUJwUWR2WDNKWUJGTW93SEszVmd3ZXRMcXhkQjRneTBFR25ZeGpGcmlTMDV0MDRRSGFNdHRIQ3M5bHJOb08rN1J0NkUwaEpVOU1SdDRIMkc0WnI5MXV1NXhrKy9MVmhQWUZJZXUyMjIycTZYckdiREJIckRCRjVYMzk1L3Z3NVB4dE83Mi9PLzNYYjdVMzhIeHpoUm83L005cTY5c3ovL1I2ZnYzNjN1NDZqWFdlMjNQV1gxNVhWWFhJWkxwczdzd1V5QlJYSGp2MU9TNjE0UUo2UzJjSlhLNWQyZkRtZk9Xb0ZTYXhhQ1dPMXNySVQraWdPM1NzL1VTdEFFMVlCMElHZElBb1g1YWQyaFhXQUZOWkNFbHV4NHdxZU5meTNYRGQzV3ZEYVAvTEhVM3dxVjVIT1cxN0J2N2JuYTVpTFdoa2RINThjZlJqdlcvdmp2Y25wNU9odzU4MW9PamFWWFNCY0d5bjBMaVhUTUUxbGVQTCtNRmU2UVAxMmdjOU1vbkJPYSt6QVNWWnhnWXV0SXNEVTBQbTVOdGlwd0NjMktlQWE5RStWL1JxOXR0NGZUajZxN09mcDBkNFAxdW4wWkR4NlZ4dkdRRmdUWEpCd25WUU5EUjlBWDB2ZlRVamp0TURTdzg2cXVGQU5iNzFZeFZYb1U0MzlsVTNPZ2Rpc0tpcjhiNkRVYWkrVm41WktyZUV2M2REenE3WGEwRmtIcHFNb1pIdzNsekNyaW9ORktzc1FsbTVaZ2RkMDdQajVZc2FOeUhldnE1MTJ1OW1wcGM5bkFTbitaZUJFdm4yVlBvYTZMODB2ZE9ZTmR4N0cwT0V3OHBOMXRDUkkxWmlIdGhkWG9WZ2pYczFueVJ6V0w2N1d6clR6R2dFaHJrRTFzZU1yMVpsNUttQ21yYzV0eDU4emFDYXh5Ykcxa1g1WmhqZlY5QWYrOHlVRUpteWR1TFhHTEE2RE1GcllTVFlLc2tpSUR1cFhCYkFXb0RVTGx3Q25EK09UeWV0UDF1aHczenFkdkRrRTJPRXdySm1uRE1oNEZDSUJrTjg0Tk1XT2tsbGd1NGtWWDlvZ1pDc0R0bmthOURlT3lLNDFMdjFiYjNZQktGK3RxUXBPRHZpNUVMY1A5SGo2NlhENmRqeWQ3RmtIUjN1akErdURyZ2pOQXFzSlBaRXQyb0R2YlBWb3E1NVBseExHQ05NRkdyZFl3U2hqVlZtR1FPR2g2WXU2OHBMQTdhVUMzeDRhMmRsQTc1emYwd1dJL005Vk8wblVjRVdnYng0Q0xPa1NtTXF0d3BZQklQNmtkUmlHcGdSc2FGeUJqdGJRT3dHb0Vrbmp4ZGNwOEdFd1orbXZjM0VaeUp2MDUzbkprcEFTK2FmbjJIaDA0U2Q4S2VnUVNsZURyQmkwZ2pDbVEwZllwR0RPRDdzTTJsVUFpNGlIVUV6WWkvSXlHQm9NYmhiSGEyRDI3VVFaNUtxcWluKzdta1YrVEY1aXd5OGxlSHYrUExHcmk5bHlEUU0yalpxRS8vYzdiTnZpc2xabU1kbSt1THFEOEV6R3VuUHpBYlFqTFluYkNjaWxHbEw4V2RpelpaV2hDWXgwUFljdCs1WDJmVE5MTHRQam96SDFrV3JiMGQwK3pNZ0ZrblZYcmVFNWtYZ1o4Y0ZsQjh5QmZ1YzJpTXJrN0lpVndSbEFpU3lJYXdIbjYxNlJSL2ZERzFNK01xcUpwMklMdVBYSlFNNlVNQWlRNGxqQUZLMWRHRC9DZVFZVEZnK242azNEdi9WZGdHRkpSVHpxMXNscW5VQ2xLanNiRzhmd0Z6cXI3U3A0bENtN1NueTNUQzVoWFZ4VXV3SHBCUktKZzcrRlpURE43RzA5dkFLeXU1UE9sS0I1UFdYYTZtbEJaV2liQXFYL3FzUXc3NFdORzUwZFQxbWJmQ2wzcnhHQlYzWU0wSmxHYS84ZXpwb29zYTc4dTlqRTMrVm5SWXFaUStkWDk2Z3ExM1kwczVlQXE0cWpQTEYvQXBVTDI4d09CQUZ1dHFMYXNOMlYydkRDS1MvaEtLb0R0RUlSbHBEdVpWaTNDN3NCdTcrcWhGZEtEVGNDamlaWHpNRmlUckVZMzBPRlJqT2NCUUlCUGNDV0VxakdlZFk4UExxZ3crQ1VWam1kanQ2TXJiMmpkOGRIaCtQREtaL2J0a0V5bFpuY3p1UVFXam80RUZ0aWhQdUIxbUR0WnRjY09tbHpvNzNwNUFPY2swOXY3OUszNThtbDNCcVFDT3Z0ZUhRd2ZXc0JiL1o2Y2pEZTNsbzVwSjBDcEowSElPMXNoVFRGa2NkQTJua2NwTXRib3dCNUZEQWtsR1VzNWh6SUZJTnBZTS9tUUxaZ01QU0IzTmxyZXg3RDJCMmhwNk9EZzFjallDNUxoNXIxaEwwNHRudEY1N2tKODlQaWpQOTJ3alh3b2RFZDFPSE1kNVdRNjFrTWkwSE8xUUlycmtwYzErVGQ4Y0g0SFJtV3dsdXpnRnpHNU8zaCtFZHJkTEwzZGpJZDcwM2ZuNHlWZXdaZDNvV0M5SlMzYkoyTS8rdjk1R1M4cjVRT05nTENEU1Q4VzR5MWRCaWo5OU8zUnllVGYvSCt3eXNUejBZMmpBYjJpYXd1TUVQcnhDd2hxQ1YwdjU2SjdTSnhEYStRZlNMTktnUDI1WDRJRXNveWtRU0NkWktqdWJXVUM5WndiNFZYRlI4UXBtTHN3QS9MV3RvTDM3SmdKcGFGcDdobFFlUDJETjZmRWszUStIYVdWT254WG50Vytmd3YwLytJZHl4LytSMzFQMDJ0byt0NS9VOUxiei9yZi81NC9jODJiYy9xeGxNcjhTVlF6RG44WFRzZ0tybCtEQ1hpTy9nSGdFcFVRTlBSNlErTWE5WDBkNXJlbnI3dWFoL2U2dU85Y2NmNDlQSGtuODNlNFkvSzhOWDd5Y0crU1VXMXVxRVpIYTJudCt0YVJ4bnVIUnlkQWwxUENhNlprdFQ2bTRQalNYMDBxYjg2T3BxZVRrOUd4M1ZXdVA1QlR4dUJGbzZRS2srUi9EK3FrZGVUdzlGQlBTWGxJNnhaenhxUkd0L0JzOGM2ZlRzeUZiZmY2bm11NXJkNjhLM3BHbHFyM2V4MEFxUHQ5OXV0am1QYkhjOExtbDFmTXh5MzZ4bGV5OVk3ZGk5bzlWcDlRK3UwaGFuU1F3WUVUTkt1N211NjNXdjNlNW9CNGx1YjNCc0dkc3Z2NjU3YjYrbDJ1NjAzZmFNVHVNMm0xMjU3YmNkeC9INVQwL3M5dlFmUHV4SUE1S2FESnQ1NmRsdE9GMnJxYnJ1cmU0N24rbjdRYmpiNzhLQUxQNExBNjNVMHJ4ZjRNT09nNWNGeDQvZHRvK3MwQTA4WkFzQU9UNCtQVHFhNWx0czkzK2tHUnF2aisxclR0Z01OQm9WVW9HVm9tdGYyZXUzQTdmaU9aclRnbWR2cWExN0g5cjJtWjd0ZHh6UDBma3ZaT1lIMU1DWHhTZGtGWVdFWGZ1NFd6MFBVSXlIVFU5dEZoQnNlano0ZEhJMzJUV3hrRjQ3RU85UXBOUUFuR3hkZmxDRWV3K3lWdlFaOGoyWmZ5QUZPcm8wUVhJZW43OThCeGsxT25qQ0FjQm12UWI0RzZSNUhRTVI4Z3RTMXRMMS9uZ0xpQ1kzdktxd1M2M2Y2a1EyS1hNb2l4dzNveVZyWk9Sa2ZqRWVuNC95QXdsV1NEZ2JtRWk3RFJiaU82eWhrN2tiK0hMZ2tQd2Fna0RhR2UrOVBUZ0NobjlLR3U0NGlIOFN6MnZEOTRXUjZDbUxZUTdkWHFCSjU2RHBJS0ZOMk13Vzk3UUdQZHBvZnFKKzQwa0FYWk5WMmhTdHlxRG4rdURjK3BwdDljanA2ZFREZWYyUXpLUUd3aWswb3RaM1hrNC9BOXIwL0haOEFGREl3WkEzQXBBcjRJYnl0cVZrbGhGZFo4VHhNUWRvbEdwUDQwcTZ1bU1iazBzeHBqMnJEVEhXQ092WXFhczZBYzBkTmlhQ2xEY0tvNHFEdWRwYjRVWFZ1THh6UEhnUkU3MURWWVNOK2ovL1VWRWRSYW9QTHhucUZhcU9xSXlseUxrVlZGRlVGcnBkVk83cTRWcGt1MnV4b0t0RzNVRjV5d0NwbXAwTWpyUkVuSGxZUVhoMVBqc2Y0MkkraXdtUFVqRkNkQU8rSi9XWGRrWDhac096QXR4Yit3dkdqdUpvRURHdzQvUVZPUHdtUU1lZnZheG1BVmhtZUFDVTVEdVBaTFVHWVJRTzVYa210dldyTVlzdDI0bkMrQmlEVkt0QzIwbWdvMlB5cXNiS2pKTVpIQ3lnVjN5M29lL3d4WDE1bFB6ei9tdjVBSlZzVm4rQjVLYnlmUmNCRk0vYjZaTDNFK1k2aktJeXF5bnFKYzZ3enNxWmtRN3ViK1hPdnNpQmd1UGFqV1hCblNRU09UeGNaK3hqQjRLOW5YclgybmFtVjloTUJkV090TTEyK1FMMFFCR1NNT09EY2M1ajFmTVluSzlaREVvZ0Y2RlJMTzZVMGNVV0kzOEtPcnZ5SURjRTFoZHNCcVVGQmQxYmphakJhRENtOTlKcTA1Tit1ZkRmeFBSQ3hVaDB5RW0xUmMwd29wcXF3YzhXU2hNQThTd0xGd3NWcTd1T1ljeVdMckFmcW9OMUwySVJFdVpqcW9Ua2ZrWFZwcjJBSGdFZ0lzcTdyejFhWnlycU1UWkNHc0xsbU9TT2dLcWtaME9hNjVTZjlmYnE1cnRScnhIOE8yd2JNY0NIdEwwQWhxbFc3QW9TN0xsMTdDVm5oNkx0S2tROHBJRHZVb1RiVHpyRU53SWRZamsrc1VCMEtaYmpzMGdiNDZrT1R1UDZJcmV4TmlnandpcUNDOE02MVZ5QlBwMHVYalNmL1FxaVRIK3JHT1lqOU1KYUNhbGh3R3lFQmZIRFRBQ3Z2elpZWGlrUzZiVW9hbHpEQ3l6Q3h3cVVQeHdUU0dMWkFuK1ZEY2xVYkxtQjMrTGN6b2szLzNLRGY2SWIrTEcxeFZLbVNyMWhNZmtFdnNUNW5HejY5WUpCTERoWm43TDVGT1RmRG1HeFk4dVl6MjY5elhvWFJqUlNubHZuREVEZ0pxRlYrZWZKU2FRQnNsQ0dWV1JwdXVMb3pxcDhKRkhhWGFoRE81K0VOSDFSc0VrVVpnT0ZNNFZDRHdTM3g5d0thaHUrZkc2aFJyTmJnajRXUEt2OVowY0p1dDR0RjFuamJKSldBSi9qaW92QUNub2dMdFdCWGJESHdRejVicDhYV2xlSXdoZGJaZXAxTG0yNUJzWW12a2dDOWRERTJyeTZzM25wSnYwclZQdU14aDlaM2l5czhCT2dQcHJVbnJWa2g0d0dHTUZuYW1wV0VWV0dsc3diSitySmhFcHpKamZFSm5RbHJTM0NGTEs2MGh1cm4yaEJ3ekwyRU5ZUFZUOWVUUFExdmx2UXBXVUtWTHhsSHhOZ1hycDZpdXhKWXBsajZPR0Q2dDZpK3E3eUdLb2RoOGhyMW0yUlBEMUNQUjNEQlg1TGpZQTNNY1JVNUVmVXloSCtBNlFVR3plT1gzakFVa01jUmhLc2JLRVFLY2szZWp0RFBELzZkMER6Qk8yREl6aFNpQkloUkM0RDkySjRIN0dtOVR1Mjd5RmQ4WEwrSXd2V0svTVF4S0hRa1dPN1NuOCtSb1UxYldZYno4QUkybTRvREFkaXk0VGJnZUFIK2xnNlB6QTc0L2dWZTBzR0NWZVBJVmIwNFVYRkJWSUMvcWFrWCtDK2JKTHlTY1I4ZTFJWWVtdWM5RmoyU3hjckVDc2dzRTJVbXRrSDRPeUFPUy84bUU5b0tpQVJqZzlvQzdzQXZNbElCY2[... ELLIPSIZATION ...]SBEZWZhdWx0IHN0YXRlPSc0NDAnOyBNaW5pbXVtIG1vZGUgb2YgdGhlIGRpcmVjdG9yeSBmaWxlIGZvciB0aGUgYWNjZXNzIHRva2VuIGZpbGUuIERlZmF1bHQgc3RhdGU9JzYwMCcuCiAgICByZXR1cm4gMAplbmNvZGluZz0ndXRmLTgnCikKICAgIG91dD1SVC8nZ2xwaS1haS1ob3N0LW9hLWV4ZWN1dG9yLnNlcnZpY2UnCiAgICBvdXQud3JpdGVfdGV4dCh1bml0KQogICAgb3MuY2htb2Qob3V0LDAoNjQ0KSkKICAgIHN1YnByb2Nlc3MucnVuKFsnL3Vzci9iaW4vc3lzdGVtY3RsJywnZGFlbW9uLXJlbG9hZCddLGNoZWNrPVRydWUpCiAgICBzdWJwcm9jZXNzLnJ1bihbJy91c3IvYmluL3N5c3RlbWN0bCcsJ3Jlc3RhcnQnLCdnbHBpLWFpLWhvc3Qtb2EtZXhlY3V0b3IudGltZXInXSxjaGVjaz1UcnVlKQogICAgcmV0dXJuIDA=')
CONTROLLER='/opt/glpi-ai-autotest/controller/autotest_controller.py';VMCONF='/etc/pve/qemu-server/105.conf';QGA_PATHS=('/var/run/qemu-server/105.qga','/run/qemu-server/105.qga')
CONSUME_DIR='/var/lib/glpi-ai-bootstrap-consumed-'+TASK+'-'+TARGET_BUILD;CONSUME_JSON=CONSUME_DIR+'/consume.json';AUTHORITY=CONSUME_DIR+'/post-consumption-recovery-authority.json';RECOVERY_PATH=CONSUME_DIR+'/post-consumption-recovery.py';TERMINAL=CONSUME_DIR+'/post-consumption-recovery-terminal.json'
ROOT='/var/lib/glpi-ai-bootstrap-closure/'+TASK;STAGED=((ROOT+'/payload.tar.gz',PAYLOAD_SHA),(ROOT+'/authorization.json',AUTH_SHA),(ROOT+'/bootstrap_installer.py',INSTALLER_SHA))

def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
class QGA:
 def __init__(self,path):self.path=path
 def call(self,cmd,args=None):
  req={'execute':cmd};
  if args is not None:req['arguments']=args
  s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);s.settimeout(10);s.connect(self.path);s.sendall((json.dumps(req,separators=(',',':'))+'\r\n').encode());buf=b''
  while b'\n' not in buf and len(buf)<16*1024*1024:
   z=s.recv(65536)
   if not z:break
   buf+=z
  s.close();obj=json.loads(buf.splitlines()[0])
  if 'error' in obj:raise RuntimeError('QGA_'+cmd)
  return obj.get('return')
def qga_path():
 for p in QGA_PATHS:
  try:
   import stat
   if stat.S_ISSOCK(os.stat(p).st_mode):return p
  except FileNotFoundError:pass
 return None
def read(q,path,maxn=32*1024*1024):
 try:h=q.call('guest-file-open',{'path':path,'mode':'r'})
 except Exception:return None
 out=bytearray()
 try:
  while len(out)<maxn:
   r=q.call('guest-file-read',{'handle':h,'count':65536}) or {};b=base64.b64decode(r.get('buf-b64',''));out.extend(b)
   if r.get('eof') or not b:break
  if len(out)>=maxn:raise RuntimeError('READ_TOO_LARGE')
  return bytes(out)
 finally:
  try:q.call('guest-file-close',{'handle':h})
  except Exception:pass
def write(q,path,data):
 h=q.call('guest-file-open',{'path':path,'mode':'w'})
 try:
  off=0
  while off<len(data):
   b=data[off:off+32768];r=q.call('guest-file-write',{'handle':h,'buf-b64':base64.b64encode(b).decode()}) or {}
   if r.get('count')!=len(b):raise RuntimeError('SHORT_WRITE')
   off+=len(b)
  q.call('guest-file-flush',{'handle':h})
 finally:q.call('guest-file-close',{'handle':h})
def exec_wait(q,path,args,timeout=480,capture=True):
 x=q.call('guest-exec',{'path':path,'arg':args,'capture-output':capture});pid=x['pid'];end=time.time()+timeout
 while time.time()<end:
  st=q.call('guest-exec-status',{'pid':pid})
  if st.get('exited'):return st
  time.sleep(.25)
 raise RuntimeError('GUEST_EXEC_TIMEOUT')
def j(b):
 try:return json.loads(b.decode()) if b else None
 except Exception:return None
def selftest():
 assert sha_bytes(RECOVERY_BYTES)==RECOVERY_SHA
 assert TASK in RECOVERY_BYTES.decode() and DECISION in RECOVERY_BYTES.decode()
 print('SELFTEST=PASS');return 0
def fail(tok,code=2):print('STATUS_TOKEN='+tok);return code
def main():
 if '--self-test' in sys.argv:return selftest()
 if os.geteuid()!=0:return fail('RECOVERY_PVE3_ROOT_CONTEXT_REQUIRED')
 try:
  hn=pathlib.Path('/etc/hostname').read_text().strip().split('.')[0]
  if hn!='pve3':return fail('RECOVERY_PVE3_HOST_MISMATCH')
  if not pathlib.Path(CONTROLLER).is_file() or sha_file(CONTROLLER)!=PVE3_SHA:return fail('RECOVERY_PVE3_CONTROLLER_PREDECESSOR_MISMATCH')
  if not pathlib.Path(VMCONF).is_file():return fail('RECOVERY_VM105_CONFIG_MISSING')
  conf=pathlib.Path(VMCONF).read_text(errors='replace')
  if 'agent:' not in conf or not any(x in conf for x in ('name: glpi-ai-mgmt-stg01','name:glpi-ai-mgmt-stg01')):return fail('RECOVERY_VM105_IDENTITY_MISMATCH')
  qp=qga_path()
  if not qp:return fail('RECOVERY_QGA_SOCKET_UNAVAILABLE')
  q=QGA(qp);q.call('guest-ping');info=q.call('guest-info');nets=q.call('guest-network-get-interfaces')
  cmds={x.get('name'):x.get('enabled',True) for x in (info.get('supported_commands',[]) if isinstance(info,dict) else [])};need=('guest-file-open','guest-file-read','guest-file-write','guest-file-flush','guest-file-close','guest-exec','guest-exec-status')
  if not all(cmds.get(n,False) for n in need):return fail('RECOVERY_QGA_CAPABILITY_UNAVAILABLE')
  ips=[a.get('ip-address') for i in (nets or []) for a in i.get('ip-addresses',[])]
  if '192.168.200.201' not in ips:return fail('RECOVERY_VM105_IP_MISMATCH')
  c=j(read(q,CONSUME_JSON,1024*1024))
  if not isinstance(c,dict) or c.get('task_id')!=TASK or c.get('build_id')!=TARGET_BUILD or c.get('capsule_sha256')!=CAPSULE_SHA or c.get('payload_sha256')!=PAYLOAD_SHA or c.get('consumed') is not True:return fail('RECOVERY_CONSUMPTION_MARKER_MISMATCH')
  # Read-only stage validation before recovery authority is consumed. Missing is recoverable; mismatch is not.
  for p,expected in STAGED:
   b=read(q,p)
   if b is not None and sha_bytes(b)!=expected:return fail('RECOVERY_STAGED_BYTES_MISMATCH')
  if sha_bytes(RECOVERY_BYTES)!=RECOVERY_SHA:return fail('RECOVERY_PROGRAM_LOCAL_SHA_MISMATCH')
  old=read(q,AUTHORITY,1024*1024)
  if old is not None:return fail('RECOVERY_AUTHORITY_ALREADY_CONSUMED')
  marker={'schema':'glpi-ai-post-consumption-recovery-authority/v1','task_id':TASK,'target_build_id':TARGET_BUILD,'recovery_build_id':RECOVERY_BUILD,'decision_id':DECISION,'decision_sha256':DECISION_SHA,'approval_receipt_sha256':APPROVAL_SHA,'recovery_program_sha256':RECOVERY_SHA,'consumed':True}
  # FIRST RECOVERY MUTATION: durable single-use authority marker in already-existing consumed directory.
  write(q,AUTHORITY,(json.dumps(marker,sort_keys=True,separators=(',',':'))+'\n').encode())
  write(q,RECOVERY_PATH,RECOVERY_BYTES)
  st=exec_wait(q,'/usr/bin/python3',[RECOVERY_PATH],600,True)
  tb=read(q,TERMINAL,4*1024*1024);to=j(tb)
  if isinstance(to,dict):
   print('STATUS_TOKEN='+str(to.get('state','RECOVERY_TERMINAL_UNKNOWN')))
   dp=to.get('drive_publication') or {};print(json.dumps({'state':to.get('state'),'reason_code':to.get('reason_code'),'drive_publication':dp},sort_keys=True,separators=(',',':')))
   return 0 if str(to.get('state','')).startswith('RECOVERED_') else 2
  out=base64.b64decode(st.get('out-data','')).decode(errors='replace') if st.get('out-data') else ''
  for line in out.splitlines():
   if line.startswith('STATUS_TOKEN='):print(line);break
  else:print('STATUS_TOKEN=RECOVERY_EXECUTED_WITHOUT_TERMINAL_RECEIPT')
  return 2
 except Exception as e:
  print('STATUS_TOKEN=RECOVERY_LAUNCHER_FAILED_'+type(e).__name__.upper());return 4
if __name__=='__main__':raise SystemExit(main())
