from typing import Optional, List
from cuml.ensemble import RandomForestClassifier as CumlRandomForestClassifier
from ._core import get_feature_importance_f, get_feature_importance_d

class RandomForestClassifier(CumlRandomForestClassifier):
  
  @property
  def feature_importances_(self) -> Optional[List[float]]:
    if self.rf_forest:
      return get_feature_importance_f(self.rf_forest, self.n_cols)
    elif self.rf_forest64:
      return get_feature_importance_d(self.rf_forest64, self.n_cols)
    
    return None