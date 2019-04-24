# ATF

tools for processing the outputof of FreeEnCal 3.2

- clean: clean the formula in Logical Premises and Empirical Premises.

- cmp: compare outfiles with previous FEC files(standard) for checking.

- autoNBG: batch execution of NBG set theory.

- predicateLogicConvert: convert the prefix form of FreeEnCal language to infix of predicate Logic.

- propositionalLogicConvert: convert the prefix form of FreeEnCal language to infix of propositional Logic.


## 入力ファイルの形式

### 論理定理導出モードと経験定理導出モード

- 論理定理導出モード
  入力ファイルのEmpiricalPremises という欄を空っぽ（記載しない）場合は、論理定理導出モードで動きます。
  論理定理導出モードでは LogicalPremises に記載されている論理定理を推論規則の適用対象とし、論理定理フラグメントを導出します。
  如果输入文件的EmpiricalPremises字段为空（未显示），则它将以逻辑定理推导模式启动。 在逻辑定理推导模式中，将LogicalPremises中描述的逻辑定理应用于推理规则，并导出逻辑定理片段。
- 経験定理導出モード
  入力ファイルのEmpiricalPremises という欄に論理式が記載されている場合は、経験定理導出モードで動きます。
  経験定理導出モードでは LogicalPremises に記載されている論理定理同士を推論規則の適用対象としません（論理定理だけを用いて、式を導出することはしません）。
  如果在输入文件的EmpiricalPremises字段中描述了逻辑表达式，它将在经验定理推导模式中移动。 在经验定理推导模式中，LogicalPremises中描述的逻辑定理不受推理规则的约束（我们不使用逻辑定理推导表达式）

## 入力ファイルの書式 

推論規則（InferenceRule）、論理体系（LogicalPremise）、論理結合子の入れ子度合いの制限（Degree）は、必ず記載されていなければななりません。その他は任意です

```
InferenceRule IR_NUMBER
_INFERENCE_RULE_
_INFERENCE_RULE_
LogicalPremise LP_NUMBER
_WFF_
_WFF_
_WFF_
_WFF_
Degree LC_NUMBER
_LIMIT_OF_DEGREE_
_LIMIT_OF_DEGREE_
_LIMIT_OF_DEGREE_
_LIMIT_OF_DEGREE_
EliminationRule ER_NUMBER
_ELIMINATION_RULE_
_ELIMINATION_RULE_
_ELIMINATION_RULE_
_ELIMINATION_RULE_
EmpiricalPremise EP_NUMBER
_WFF_
_WFF_
_WFF_
```



## 