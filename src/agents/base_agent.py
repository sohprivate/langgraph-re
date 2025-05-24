#!/usr/bin/env python3
"""
ベースエージェントクラス
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from loguru import logger


class BaseAgent(ABC):
    """全エージェントの基底クラス"""
    
    def __init__(self, name: str, description: str, **kwargs):
        self.name = name
        self.description = description
        self.config = kwargs
        logger.info(f"Initialized {self.name} agent")
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """エージェントの主要処理を実行"""
        pass
    
    async def preprocess(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """前処理（オーバーライド可能）"""
        return input_data
    
    async def postprocess(self, output_data: Dict[str, Any]) -> Dict[str, Any]:
        """後処理（オーバーライド可能）"""
        return output_data
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """エージェント実行のメインフロー"""
        try:
            logger.info(f"Running {self.name} agent")
            
            # 前処理
            processed_input = await self.preprocess(input_data)
            
            # 主要処理
            result = await self.execute(processed_input)
            
            # 後処理
            final_result = await self.postprocess(result)
            
            logger.success(f"{self.name} agent completed successfully")
            return final_result
            
        except Exception as e:
            logger.error(f"Error in {self.name} agent: {e}")
            raise
    
    def __str__(self) -> str:
        return f"{self.name}Agent({self.description})"
    
    def __repr__(self) -> str:
        return self.__str__()
