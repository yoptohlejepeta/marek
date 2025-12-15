local fileUtils = require("src.file_utils")

---@class Preview
---@field currentImageIdx integer defaults to 1
---@field allImages love.Image[]?
local Preview = {
  currentImageIdx = 1,
  allImages = {}
}


function Preview:new()
  local obj = setmetatable({}, self)
  self.__index = self
  return obj
end

--- Opens file dialog and appends selected images to self.allImages
function Preview:appendImages()
  local appendImage = function(fileData)
    local im = love.graphics.newImage(fileData)
    table.insert(self.allImages, im)
  end

  fileUtils.processFiles(appendImage)
end

function Preview:draw()
  local preview_start = love.graphics.getWidth() * 0.15

  if self.allImages and self.allImages[self.currentImageIdx] then
    local currImage = self.allImages[self.currentImageIdx]
    love.graphics.draw(currImage, preview_start)
  end
end

return Preview

