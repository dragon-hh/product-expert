# 数据契约

## GDP 本地数据底座

`workspace-product-expert/data/` 就是本项目搭建的本地 GDP，索引文件是 `workspace-product-expert/data/catalog.json`。客户主动导入、飞书聊天/表格提取、附件解析、人工补录、FAE 服务记录和 EMS/监控导出数据，最终都归一化进入这个本地 GDP。

`records` 为空只表示尚未导入真实数据，不表示该表缺失。业务技能可以读取 schema 判断字段要求，但不能基于空 records 输出正式业务结论。

| 逻辑表 | 本地文件 | 主键 | 对应原始需求 |
| --- | --- | --- | --- |
| 客户需求主表 | `data/demand_master.json` | `demand_id` | `realTask.md` 6.1 |
| 方案主表 | `data/solution_master.json` | `solution_id` | `realTask.md` 6.2 |
| 储能 ROI 测算主表 | `data/roi_measurement.json` | `roi_id` | `realTask.md` 6.3 |
| 客户画像表 | `data/customer_profile.json` | `customer_id` | 客户主数据和画像补充 |
| 订单/商机主表 | `data/order_master.json` | `order_id` | 订单转化补充 |
| 交付项目表 | `data/delivery_project.json` | `delivery_id` | 交付 9 件套输入补充 |
| 现场勘查表 | `data/site_survey.json` | `survey_id` | 交付现场条件补充 |
| 文档索引表 | `data/document_library.json` | `document_id` | 需求、方案、客户确认、合同、验收和运维文档路径 |
| 客户赋能记录表 | `data/enablement_records.json` | `enablement_id` | 客户赋能和客户承认过程补充 |
| FAQ 记录表 | `data/faq_records.json` | `faq_id` | 知识库、FAQ 和专家修正补充 |
| FAE/服务记录表 | `data/service_records.json` | `service_id` | 服务、故障、专家转接和 FAQ 候选补充 |
| ROI 参数表 | `data/roi_parameter.json` | `parameter_id` | 电价、负荷、成本、补贴和假设补充 |
| 储能运行数据表 | `data/operation_data.json` | `operation_id` | 实际运行回流和 ROI 校准补充 |
| 模板使用记录表 | `data/template_usage.json` | `usage_id` | 模板复用率和退回分析补充 |
| 标准包使用记录表 | `data/standard_package_usage.json` | `usage_id` | 标准包匹配和复用分析补充 |
| 数据同步运行记录 | `data/sync_runs.json` | `run_id` | 定时同步运行日志 |

### 原始 GDP 三张主表字段

`demand_master.json` 必须覆盖：需求编号、客户名称、客户画像、销售负责人、业务部门、市场区域、项目名称、项目背景、业务痛点、建设目标、应用场景、年度需求总量、年度建设节奏、采购计划、是否储能项目、储能项目类型、ROI 数据完整度、需求完整度评分、是否允许生成方案、缺失信息、需求说明书。

`solution_master.json` 必须覆盖：方案编号、关联需求编号、客户名称、项目名称、产品线、业务线、应用场景、方案类型、Word 模板编号、是否包含 ROI、ROI 测算编号、方案状态、客户赋能状态、客户承认状态、是否转订单、订单编号、订单金额、未转化原因、方案版本、方案附件、风险等级。

`roi_measurement.json` 必须覆盖：测算编号、客户名称、项目名称、方案编号、储能类型、所在地区、储能功率、储能容量、项目总投资、年度总收益、年度净收益、静态回收期、动态回收期、ROI、IRR、NPV、测算等级、收益口径、测算版本、测算状态、审核人、创建时间。

## Demand Record JSON

```json
{
  "demand_id": "D-YYYYMMDD-001",
  "customer": {"name": "", "industry": "", "region": "", "scale": "", "level": "", "contacts": [], "decision_chain": []},
  "project": {"name": "", "background": "", "pain_points": [], "goals": [], "scope": "", "functional_requirements": [], "technical_requirements": [], "certification_requirements": [], "timeline": ""},
  "scenario": {"primary": "新建|替换|扩容|改造|集成|试点|投标|年度框架|未知", "confidence": 0.0, "evidence": []},
  "annual_demand": {"total": "", "phase_plan": [], "regions": [], "product_lines": []},
  "procurement_plan": {"timeline": "", "method": "", "budget_status": "", "quote_node": "", "contract_node": ""},
  "storage": {"is_storage_project": false, "type": "户用储能|工商储|未知", "roi_prerequisites": {}, "roi_data_completeness": 0.0},
  "risks": [],
  "constraints": [],
  "source": []
}
```

## Review Status

Use one of: `draft`, `needs_sales_input`, `needs_solution_review`, `needs_product_review`, `needs_roi_review`, `approved_internal`, `approved_external`, `blocked`.

## Delivery Handoff Input JSON

`delivery-handoff-skill` 的最小输入是 `solution_id` 或 `order_id`。字段可以由用户本次输入、方案主表、订单系统、方案附件、交付人员表和现场勘查记录共同补齐。

```json
{
  "solution_id": "",
  "order_id": "",
  "demand_id": "",
  "customer": {
    "name": "",
    "contacts": [],
    "customer_side_owners": []
  },
  "project": {
    "name": "",
    "site": "",
    "accepted_solution_status": "未提交|已提交|已承认|需修改|未承认",
    "solution_version": "",
    "solution_attachment": ""
  },
  "order": {
    "status": "",
    "amount": "",
    "procurement_plan": "",
    "contract_node": "",
    "delivery_scope": ""
  },
  "configuration": {
    "product_lines": [],
    "bom": [],
    "software_versions": [],
    "quantities": []
  },
  "delivery": {
    "included_items": [],
    "excluded_items": [],
    "customer_prerequisites": [],
    "acceptance_requirements": [],
    "delivery_owner": "",
    "fae_owner": "",
    "after_sales_owner": ""
  },
  "site_survey": {
    "power": "",
    "network": "",
    "grid_connection": "",
    "fire_safety": "",
    "environment": "",
    "access_conditions": ""
  },
  "storage": {
    "is_storage_project": false,
    "charge_discharge_strategy": "",
    "ems_parameters": {},
    "monitoring_requirements": [],
    "operation_data_fields": []
  },
  "field_sources": {
    "solution": "",
    "order": "",
    "configuration": "",
    "delivery": "",
    "site_survey": "",
    "storage": ""
  }
}
```

## Evidence Rules

Prefer table row IDs, document links, file paths, timestamps and reviewer names. Do not promote unverified model inference to confirmed fact.
