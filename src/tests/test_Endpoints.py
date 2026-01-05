import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from src.app import app, displayQueue
from src.models.DisplayData import DisplayData

baseUrl = "http://test"
displayUrl = "/display"

@pytest.mark.asyncio
async def test_AppEndpoints_DisplayEndpointRecievesHTTPPUTRequestWithAllBodyParameters_ItemIsPutInQueue():
    async with AsyncClient(transport=ASGITransport(app=app),base_url=baseUrl) as client:
        await client.post(url=displayUrl, json={
            "message": "testing",
            "sprite": "VGhlc2UgYXJlbid0IHRoZSBkcm9pZHMgeW91J3JlIGxvb2tpbmcgZm9y",
            "spriteReplayTimes": 2
        })
        item = await displayQueue.get()
        assert item.model_dump() == DisplayData(message="testing",sprite="VGhlc2UgYXJlbid0IHRoZSBkcm9pZHMgeW91J3JlIGxvb2tpbmcgZm9y",spriteReplayTimes=2).model_dump()
        
        
@pytest.mark.asyncio
async def test_AppEndpoints_DisplayEndpointRecievesHTTPPUTRequestWithOnlyRequiredParameters_ItemIsPutInQueueWithDefaultValuesForUnspecifiedFields():
    async with AsyncClient(transport=ASGITransport(app=app),base_url=baseUrl) as client:
        await client.post(url=displayUrl, json={
            "message": "testing"
        })
        item = await displayQueue.get()
        assert item.model_dump() == DisplayData(message="testing",sprite=None,spriteReplayTimes=1).model_dump()
        
        
@pytest.mark.asyncio
async def test_AppEndpoints_DisplayEndpointRecievesHTTPPUTRequestWithoutRequiredParameters_ItemIsNotPutInQueueAndAnErrorIsReturned():
    async with AsyncClient(transport=ASGITransport(app=app),base_url=baseUrl) as client:
        result = await client.post(url=displayUrl, json={
        })
        assert displayQueue.empty()
        assert result.status_code == 422