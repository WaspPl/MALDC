import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from src.app import app, displayQueue
from src.models.DisplayData import DisplayData

baseUrl = "http://test"
displayUrl = "/display"

@pytest.mark.asyncio
async def test_AppEndpoints_PUTRequestWithAllBodyParameters_ItemIsPutInQueue():
    async with AsyncClient(transport=ASGITransport(app=app),base_url=baseUrl) as client:
        await client.post(url=displayUrl, json={
            "message": "testing",
            "spriteBase64": "iVBORw0KGgoAAAANSUhEUgAAAGgAAAAICAYAAAAV6Lr7AAACkklEQVR4AeTVPWsUURSA4TuBIAr+ASEuWlhIQGIjSCxsxCIxlSJaGksrO3+AjViIpWsjKIqVmiLYWBgECw1CCGihLIHUfoBiNc4zcJeT2Z2YxY8UCXlzzz3vvWdn75mZjKXwc/DJTInuu075cH2iDKoOOSwsd0rUyfCHw/LrTuvesLwfnnl+pf7cfqIlUBstup+2Rs1+ohHMLp4rr764XM4uXhy4zsbSbZ9uaNDk7gMJ80d6xfl9a0Xz6jjMTPUKtPmpY73iVdXE6O2DnAZGv/Ljk3Ta7FAtsB/iNn5XQ2NSGm/b3s8/rq7/7sqJbW/gWP+KqsBBoQqH/nIYKqskhypMx6smGjPycHdrYPQf5xYKB5+9PZpojPCIuWbMq/X01O2BG8wT8+Hn93Ro15508+Sd4tnp+wNr1NtKY4Zdn71/m7pBXmfd6rXmi6H5IV5n4ND05i6Yg3kmPym5CU1vn7UOlIO5JtoLc3AQ2xednKeHV8vcGmNGY6A5OdccPTlyZ6sb7NLky6ENVLfcO5GM1kbk3q5Ol8aYz7H8KL5ukNeZ15q7D7lYHr3OwCHn8+igHCiHnDd6UlyUmIM4Y1+btxfqW2Mv7LWPEw/z8tYYs/f0QC6itrnmfB3fnzZrjMO19ujhpSLXN89oHGfMdbMzyo/i6wZ1L0yXuPboc4IYCkIMDmJwWL0xkcw5iMHhza0/8+qroTbUhtrYqp+710uIezVPbbkv1fcor2/8t+OQOVhXfFtLzcZwGd41aUJel51xVF83aP7BUvG+t54icj4I4ujEchzEchE5DuLoxHIcxHIROQ7i6MRyHMRyETkO4ujEDovzFDY9B94hR69JHHj8S183yIfsNBxq23fWwDbP4X/5XwAAAP//LrH8uQAAAAZJREFUAwAS58ejK7uBhAAAAABJRU5ErkJggg==",
            "spriteReplayTimes": 2
        })
        item = await displayQueue.get()
        assert item.model_dump() == DisplayData(message="testing",
                                                spriteBase64="iVBORw0KGgoAAAANSUhEUgAAAGgAAAAICAYAAAAV6Lr7AAACkklEQVR4AeTVPWsUURSA4TuBIAr+ASEuWlhIQGIjSCxsxCIxlSJaGksrO3+AjViIpWsjKIqVmiLYWBgECw1CCGihLIHUfoBiNc4zcJeT2Z2YxY8UCXlzzz3vvWdn75mZjKXwc/DJTInuu075cH2iDKoOOSwsd0rUyfCHw/LrTuvesLwfnnl+pf7cfqIlUBstup+2Rs1+ohHMLp4rr764XM4uXhy4zsbSbZ9uaNDk7gMJ80d6xfl9a0Xz6jjMTPUKtPmpY73iVdXE6O2DnAZGv/Ljk3Ta7FAtsB/iNn5XQ2NSGm/b3s8/rq7/7sqJbW/gWP+KqsBBoQqH/nIYKqskhypMx6smGjPycHdrYPQf5xYKB5+9PZpojPCIuWbMq/X01O2BG8wT8+Hn93Ro15508+Sd4tnp+wNr1NtKY4Zdn71/m7pBXmfd6rXmi6H5IV5n4ND05i6Yg3kmPym5CU1vn7UOlIO5JtoLc3AQ2xednKeHV8vcGmNGY6A5OdccPTlyZ6sb7NLky6ENVLfcO5GM1kbk3q5Ol8aYz7H8KL5ukNeZ15q7D7lYHr3OwCHn8+igHCiHnDd6UlyUmIM4Y1+btxfqW2Mv7LWPEw/z8tYYs/f0QC6itrnmfB3fnzZrjMO19ujhpSLXN89oHGfMdbMzyo/i6wZ1L0yXuPboc4IYCkIMDmJwWL0xkcw5iMHhza0/8+qroTbUhtrYqp+710uIezVPbbkv1fcor2/8t+OQOVhXfFtLzcZwGd41aUJel51xVF83aP7BUvG+t54icj4I4ujEchzEchE5DuLoxHIcxHIROQ7i6MRyHMRyETkO4ujEDovzFDY9B94hR69JHHj8S183yIfsNBxq23fWwDbP4X/5XwAAAP//LrH8uQAAAAZJREFUAwAS58ejK7uBhAAAAABJRU5ErkJggg==",
                                                spriteReplayTimes=2).model_dump()
        
        
@pytest.mark.asyncio
async def test_AppEndpoints_PUTRequestWithOnlyRequiredParameters_ItemIsPutInQueueWithDefaultValuesForUnspecifiedFields():
    async with AsyncClient(transport=ASGITransport(app=app),base_url=baseUrl) as client:
        await client.post(url=displayUrl, json={
            "message": "testing"
        })
        item = await displayQueue.get()
        assert item.model_dump() == DisplayData(message="testing",
                                                spriteBase64=None,
                                                spriteReplayTimes=1).model_dump()
        
        
@pytest.mark.asyncio
async def test_AppEndpoints_PUTRequestWithoutRequiredParameters_ItemIsNotPutInQueueAndAnErrorIsReturned():
    async with AsyncClient(transport=ASGITransport(app=app),base_url=baseUrl) as client:
        result = await client.post(url=displayUrl, json={
        })
        assert displayQueue.empty()
        assert result.status_code == 422