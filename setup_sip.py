import asyncio
from livekit import api


async def main():
    lk = api.LiveKitAPI(
        url='wss://voice-recorder-uvglc4lk.livekit.cloud',
        api_key='APIuteW4naJyQQn',
        api_secret='oUJZjfpfEmFFZAggKQgSoA9DjQtOMXsoRGos1XWXUWl'
    )

    rule = await lk.sip.create_sip_dispatch_rule(
        api.CreateSIPDispatchRuleRequest(
            rule=api.SIPDispatchRule(
                dispatch_rule_individual=api.SIPDispatchRuleIndividual(
                    room_prefix="call-",
                )
            ),
            trunk_ids=["ST_Ltg2uZgBYuHk"],
            name="Inbound Call Rule",
        )
    )
    print('Dispatch Rule ID:', rule.sip_dispatch_rule_id)
    await lk.aclose()


asyncio.run(main())
